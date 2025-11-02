package auth

import (
	"errors"
	"time"

	"github.com/golang-jwt/jwt/v5"
	"github.com/google/uuid"
)

var (
	ErrInvalidToken = errors.New("invalid token")
	ErrExpiredToken = errors.New("expired token")
)

// TokenClaims represents the JWT claims
type TokenClaims struct {
	UserID         uuid.UUID `json:"user_id"`
	Email          string    `json:"email"`
	OrganizationID *uuid.UUID `json:"organization_id,omitempty"`
	jwt.RegisteredClaims
}

// TokenPair represents access and refresh tokens
type TokenPair struct {
	AccessToken  string `json:"access_token"`
	RefreshToken string `json:"refresh_token"`
	ExpiresIn    int64  `json:"expires_in"`
}

// GenerateTokenPair creates both access and refresh tokens
func GenerateTokenPair(userID uuid.UUID, email string, organizationID *uuid.UUID, jwtSecret string, accessTTL, refreshTTL time.Duration) (*TokenPair, error) {
	// Generate access token
	accessToken, err := generateToken(userID, email, organizationID, jwtSecret, accessTTL)
	if err != nil {
		return nil, err
	}

	// Generate refresh token (longer TTL)
	refreshToken, err := generateToken(userID, email, organizationID, jwtSecret, refreshTTL)
	if err != nil {
		return nil, err
	}

	return &TokenPair{
		AccessToken:  accessToken,
		RefreshToken: refreshToken,
		ExpiresIn:    int64(accessTTL.Seconds()),
	}, nil
}

// generateToken creates a JWT token
func generateToken(userID uuid.UUID, email string, organizationID *uuid.UUID, jwtSecret string, ttl time.Duration) (string, error) {
	now := time.Now()
	claims := TokenClaims{
		UserID:         userID,
		Email:          email,
		OrganizationID: organizationID,
		RegisteredClaims: jwt.RegisteredClaims{
			ExpiresAt: jwt.NewNumericDate(now.Add(ttl)),
			IssuedAt:  jwt.NewNumericDate(now),
			NotBefore: jwt.NewNumericDate(now),
		},
	}

	token := jwt.NewWithClaims(jwt.SigningMethodHS256, claims)
	return token.SignedString([]byte(jwtSecret))
}

// ValidateToken validates and parses a JWT token
func ValidateToken(tokenString, jwtSecret string) (*TokenClaims, error) {
	token, err := jwt.ParseWithClaims(tokenString, &TokenClaims{}, func(token *jwt.Token) (interface{}, error) {
		// Verify signing method
		if _, ok := token.Method.(*jwt.SigningMethodHMAC); !ok {
			return nil, ErrInvalidToken
		}
		return []byte(jwtSecret), nil
	})

	if err != nil {
		if errors.Is(err, jwt.ErrTokenExpired) {
			return nil, ErrExpiredToken
		}
		return nil, ErrInvalidToken
	}

	claims, ok := token.Claims.(*TokenClaims)
	if !ok || !token.Valid {
		return nil, ErrInvalidToken
	}

	return claims, nil
}
