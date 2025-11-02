package services

import (
	"errors"
	"time"

	"github.com/google/uuid"
	"publicscannerapi/internal/models"
	"publicscannerapi/internal/repository"
	"publicscannerapi/pkg/auth"
)

var (
	ErrInvalidCredentials = errors.New("invalid credentials")
	ErrUserInactive       = errors.New("user account is inactive")
)

// AuthService handles authentication business logic
type AuthService struct {
	userRepo   *repository.UserRepository
	jwtSecret  string
	accessTTL  time.Duration
	refreshTTL time.Duration
}

// NewAuthService creates a new authentication service
func NewAuthService(userRepo *repository.UserRepository, jwtSecret string, accessTTL, refreshTTL time.Duration) *AuthService {
	return &AuthService{
		userRepo:   userRepo,
		jwtSecret:  jwtSecret,
		accessTTL:  accessTTL,
		refreshTTL: refreshTTL,
	}
}

// RegisterRequest represents a registration request
type RegisterRequest struct {
	Email     string `json:"email" binding:"required,email"`
	Password  string `json:"password" binding:"required,min=8"`
	FirstName string `json:"first_name" binding:"required"`
	LastName  string `json:"last_name" binding:"required"`
}

// LoginRequest represents a login request
type LoginRequest struct {
	Email    string `json:"email" binding:"required,email"`
	Password string `json:"password" binding:"required"`
}

// AuthResponse represents authentication response
type AuthResponse struct {
	User   *models.User      `json:"user"`
	Tokens *auth.TokenPair   `json:"tokens"`
}

// Register registers a new user
func (s *AuthService) Register(req *RegisterRequest) (*AuthResponse, error) {
	// Hash password
	hashedPassword, err := auth.HashPassword(req.Password)
	if err != nil {
		return nil, err
	}

	// Create user model
	user := &models.User{
		ID:           uuid.New(),
		Email:        req.Email,
		PasswordHash: hashedPassword,
		FirstName:    req.FirstName,
		LastName:     req.LastName,
		IsActive:     true,
	}

	// Save to database
	err = s.userRepo.Create(user)
	if err != nil {
		return nil, err
	}

	// Generate tokens
	tokens, err := auth.GenerateTokenPair(user.ID, user.Email, nil, s.jwtSecret, s.accessTTL, s.refreshTTL)
	if err != nil {
		return nil, err
	}

	// Clear password hash from response
	user.PasswordHash = ""

	return &AuthResponse{
		User:   user,
		Tokens: tokens,
	}, nil
}

// Login authenticates a user
func (s *AuthService) Login(req *LoginRequest) (*AuthResponse, error) {
	// Find user by email
	user, err := s.userRepo.GetByEmail(req.Email)
	if err != nil {
		if errors.Is(err, repository.ErrUserNotFound) {
			return nil, ErrInvalidCredentials
		}
		return nil, err
	}

	// Check if user is active
	if !user.IsActive {
		return nil, ErrUserInactive
	}

	// Verify password
	if !auth.CheckPassword(user.PasswordHash, req.Password) {
		return nil, ErrInvalidCredentials
	}

	// Get user's default organization (first one they're a member of)
	organizationID, err := s.userRepo.GetUserOrganization(user.ID)
	if err != nil {
		// If no organization, continue without it (organization is optional)
		organizationID = nil
	}

	// Generate tokens
	tokens, err := auth.GenerateTokenPair(user.ID, user.Email, organizationID, s.jwtSecret, s.accessTTL, s.refreshTTL)
	if err != nil {
		return nil, err
	}

	// Clear password hash from response
	user.PasswordHash = ""

	return &AuthResponse{
		User:   user,
		Tokens: tokens,
	}, nil
}

// RefreshToken refreshes an access token
func (s *AuthService) RefreshToken(refreshToken string) (*auth.TokenPair, error) {
	// Validate refresh token
	claims, err := auth.ValidateToken(refreshToken, s.jwtSecret)
	if err != nil {
		return nil, err
	}

	// Get user to verify they still exist and are active
	user, err := s.userRepo.GetByID(claims.UserID)
	if err != nil {
		return nil, err
	}

	if !user.IsActive {
		return nil, ErrUserInactive
	}

	// Generate new token pair
	tokens, err := auth.GenerateTokenPair(user.ID, user.Email, claims.OrganizationID, s.jwtSecret, s.accessTTL, s.refreshTTL)
	if err != nil {
		return nil, err
	}

	return tokens, nil
}

// GetCurrentUser retrieves the current authenticated user
func (s *AuthService) GetCurrentUser(userID uuid.UUID) (*models.User, error) {
	user, err := s.userRepo.GetByID(userID)
	if err != nil {
		return nil, err
	}

	// Clear password hash
	user.PasswordHash = ""

	return user, nil
}
