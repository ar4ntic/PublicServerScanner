import Link from "next/link";
import { Shield, Lock, Target, BarChart } from "lucide-react";

export default function Home() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-blue-50">
      {/* Header */}
      <header className="border-b bg-white/80 backdrop-blur-sm">
        <div className="container mx-auto px-4 py-4 flex justify-between items-center">
          <div className="flex items-center space-x-2">
            <Shield className="h-8 w-8 text-blue-600" />
            <span className="text-2xl font-bold">PublicScanner</span>
          </div>
          <nav className="space-x-4">
            <Link href="/login" className="text-gray-600 hover:text-blue-600">
              Login
            </Link>
            <Link
              href="/register"
              className="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700"
            >
              Get Started
            </Link>
          </nav>
        </div>
      </header>

      {/* Hero Section */}
      <main className="container mx-auto px-4 py-20">
        <div className="text-center max-w-4xl mx-auto mb-16">
          <h1 className="text-5xl font-bold mb-6 text-gray-900">
            Comprehensive Security Scanning
            <br />
            <span className="text-blue-600">For Your Public Applications</span>
          </h1>
          <p className="text-xl text-gray-600 mb-8">
            Identify vulnerabilities, security misconfigurations, and compliance
            issues before attackers do. Get actionable insights and remediation
            guidance.
          </p>
          <div className="flex justify-center space-x-4">
            <Link
              href="/register"
              className="px-8 py-3 bg-blue-600 text-white rounded-lg font-semibold hover:bg-blue-700 transition"
            >
              Start Free Trial
            </Link>
            <Link
              href="/login"
              className="px-8 py-3 border border-gray-300 text-gray-700 rounded-lg font-semibold hover:border-blue-600 hover:text-blue-600 transition"
            >
              Sign In
            </Link>
          </div>
        </div>

        {/* Features Grid */}
        <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-8 mb-16">
          <FeatureCard
            icon={<Shield className="h-10 w-10 text-blue-600" />}
            title="Port Scanning"
            description="Comprehensive TCP/UDP port scanning with service detection"
          />
          <FeatureCard
            icon={<Lock className="h-10 w-10 text-blue-600" />}
            title="SSL/TLS Analysis"
            description="Certificate validation, expiry checks, and cipher analysis"
          />
          <FeatureCard
            icon={<Target className="h-10 w-10 text-blue-600" />}
            title="Vulnerability Detection"
            description="Identify known vulnerabilities and security misconfigurations"
          />
          <FeatureCard
            icon={<BarChart className="h-10 w-10 text-blue-600" />}
            title="Compliance Reports"
            description="OWASP, CIS, PCI-DSS compliance mapping and reporting"
          />
        </div>

        {/* Security Checks */}
        <div className="bg-white rounded-xl shadow-lg p-8 max-w-4xl mx-auto">
          <h2 className="text-3xl font-bold mb-6 text-center">
            15+ Security Checks
          </h2>
          <div className="grid md:grid-cols-2 gap-4">
            {[
              "Port Scanning",
              "HTTP Security Headers",
              "SSL/TLS Certificate Analysis",
              "DNS Enumeration",
              "Directory Brute-Force",
              "WAF Detection",
              "Subdomain Enumeration",
              "Technology Stack Detection",
              "API Security Testing",
              "JavaScript Analysis",
              "Email Security (SPF/DKIM/DMARC)",
              "CORS Misconfiguration",
              "Rate Limiting Testing",
              "Cloud Service Detection",
              "Content Security Analysis",
            ].map((check) => (
              <div key={check} className="flex items-center space-x-2">
                <div className="h-2 w-2 bg-blue-600 rounded-full" />
                <span className="text-gray-700">{check}</span>
              </div>
            ))}
          </div>
        </div>
      </main>

      {/* Footer */}
      <footer className="border-t bg-white mt-20">
        <div className="container mx-auto px-4 py-8 text-center text-gray-600">
          <p>&copy; 2025 PublicScanner by Arantic Digital. All rights reserved.</p>
        </div>
      </footer>
    </div>
  );
}

function FeatureCard({
  icon,
  title,
  description,
}: {
  icon: React.ReactNode;
  title: string;
  description: string;
}) {
  return (
    <div className="bg-white rounded-lg p-6 shadow-md hover:shadow-lg transition">
      <div className="mb-4">{icon}</div>
      <h3 className="text-xl font-semibold mb-2">{title}</h3>
      <p className="text-gray-600">{description}</p>
    </div>
  );
}
