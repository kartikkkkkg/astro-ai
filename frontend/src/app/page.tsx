import Image from "next/image";
import { MapPin, Sparkles, Moon, Stars } from 'lucide-react';
import { framerMotion } from '@/lib/utils/framerMotion';

export default function Home() {
  return (
    <div className="min-h-screen bg-background font-sans dark:bg-black">
      {/* Hero Section */}
      <section className="relative min-h-[70vh] flex flex-col items-center justify-center px-6 py-20 overflow-hidden">
        {/* Cosmic Background */}
        <div className="absolute inset-0 -z-10">
          <div className="absolute inset-0 bg-[radial-gradient(circle_at_50%_50%,rgba(11,247,237,0.05)_0%,transparent_50%)]"></div>
          <div className="absolute inset-0 bg-[radial-gradient(circle_at_20%_80%,rgba(255,0,110,0.03)_0%,transparent_50%)]"></div>
          <div className="absolute inset-0 bg-[url('/api/placeholder/1920/1080')] bg-cover bg-no-repeat opacity-5"
               style={{ backgroundImage: 'url("data:image/svg+xml,%3Csvg viewBox=\\"0 0 1440 320\\" xmlns=\\"http://www.w3.org/2000/svg\\"%3E%3Cpath fill=\\"%230bf7ed%22 fill-opacity=\\"0.05\\" d=\\"M0,128L48,133.3C96,139,192,149,288,170.7C384,192,480,224,576,245.3C672,266.7,768,277.3,864,272C960,266.7,1056,245.3,1152,213.3C1248,181.3,1344,133.3,1392,109.3L1440,80L1440,320L1392,320C1344,320,1248,320,1152,320C1056,320,960,320,864,320C768,320,672,320,576,320C480,320,384,320,288,320C192,320,96,320,0,320Z\\"%3E%3C/path%3E%3C/svg%3E') }} />
          <div className="absolute inset-0 animate-orbit-slow" style={{
            backgroundImage: 'url("data:image/svg+xml,%3Csvg width=\\"60\\" height=\\"60\\" viewBox=\\"0 0 60 60\\" xmlns=\\"http://www.w3.org/2000/svg\\"%3E%3Cdefs%3E%3ClinearGradient id=\\"grad1\\" x1=\\"0%\\" y1=\\"0%\\" x2=\\"100%\\" y2=\\"0%\\"%3E%3Cstop offset=\\"0%\\" style=\\"stop-color:rgba(11,247,237,0.3)%22 /%3E%3Cstop offset=\\"100%\\" style=\\"stop-color:rgba(255,0,110,0.3)%22 /%3E%3C/linearGradient%3E%3C/defs%3E%3Ccircle cx=\\"30\\" cy=\\"30\\" r=\\"25\\" fill=\\"url(%23grad1)%22 /%3E%3C/svg%3E") }}"></div>
        </div>

        {/* Content */}
        <div className="relative z-10 max-w-4xl text-center space-y-8">
          <div className="space-y-4">
            <h1 className="text-5xl font-display bg-clip-text text-transparent bg-gradient-to-tr from-white to-[hsl(var(--accent))] sm:text-6xl">
              AstroAI
            </h1>
            <p className="text-xl text-[hsl(var(--foreground-muted))] max-w-2xl mx-auto">
              Experience the future of astrology with deterministic chart calculations powered by Swiss Ephemeris.
              Discover your cosmic blueprint with precision and clarity.
            </p>
          </div>

          <div className="flex flex-col sm:flex-row space-y-4 sm:space-y-0 sm:space-x-4 justify-center">
            <ButtonVariant
              variant="primary"
              size="lg"
              className="flex items-center justify-center space-x-3"
            >
              <Sparkles className="h-5 w-5" />
              Generate Your Chart
            </ButtonVariant>

            <ButtonVariant
              variant="outline"
              size="lg"
              className="flex items-center justify-center space-x-3 hover:bg-[hsl(var(--foreground))/0.05]"
            >
              <MapPin className="h-5 w-5" />
              Explore Features
            </ButtonVariant>
          </div>

          <div className="text-sm text-[hsl(var(--foreground-muted))]">
            <Moon className="h-4 w-4 inline-block align-middle animate-float-slow mr-2" />
            Powered by deterministic algorithms • Zero randomness • Pure calculation
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="py-20 px-6">
        <div className="max-w-5xl mx-auto text-center space-y-12">
          <h2 className="text-3xl font-bold text-[hsl(var(--foreground))]">
            Why AstroAI?
          </h2>
          <p className="text-[hsl(var(--foreground-muted))] max-w-3xl mx-auto">
            Combining ancient wisdom with modern technology to deliver the most accurate astrological insights available.
          </p>

          <div className="grid gap-8 md:grid-cols-2 lg:grid-cols-4">
            <FeatureCard
              icon={<Stars className="h-6 w-6 text-[hsl(var(--accent))] mb-4" />}
              title="Deterministic Precision"
              description="Every chart calculation follows exact astronomical algorithms with zero randomness or interpretation variance."
            />
            <FeatureCard
              icon={<Moon className="h-6 w-6 text-[hsl(var(--accent))] mb-4" />}
              title="Cosmic Design"
              description="Beautifully rendered charts with glassmorphism effects and futuristic aesthetics that feel truly celestial."
            />
            <FeatureCard
              icon={<Sparkles className="h-6 w-6 text-[hsl(var(--accent))] mb-4" />}
              title="Real-time Updates"
              description="Watch planetary movements in real-time with smooth animations and accurate transit calculations."
            />
            <FeatureCard
              icon={<MapPin className="h-6 w-6 text-[hsl(var(--accent))] mb-4" />}
              title="Location Intelligence"
              description="Precise geocoding ensures accurate house cusps and planetary positions based on your exact birth coordinates."
            />
          </div>
        </div>
      </section>

      {/* Chart Preview */}
      <section className="relative py-20 px-6 bg-[hsl(var(--background))/0.05]">
        <div className="absolute inset-0 -z-10" style={{
          backgroundImage: 'url("data:image/svg+xml,%3Csvg width=\\"60\\" height=\\"60\\" viewBox=\\"0 0 60 60\\" xmlns=\\"http://www.w3.org/2000/svg\\"%3E%3Ccircle cx=\\"30\\" cy=\\"30\\" r=\\"2\\" fill=%22%230bf7ed%22 /%3E%3C/svg%3E") }}
          style={{ opacity: '0.1' }}
        ></div>

        <div className="max-w-4xl mx-auto text-center space-y-8">
          <h2 className="text-3xl font-bold text-[hsl(var(--foreground))]">
            See Your Cosmic Blueprint
          </h2>
          <p className="text-[hsl(var(--foreground-muted))] max-w-2xl mx-auto">
            A preview of what your personalized chart will look like - combining traditional Vedic aesthetics with modern cosmic design.
          </p>

          <div className="relative">
            <div className="glass h-[500px] w-full max-w-2xl mx-auto rounded-2xl overflow-hidden relative">
              {/* Chart Background */}
              <div className="absolute inset-0" style={{
                background: 'radial-gradient(circle at center, transparent 0%, hsl(var(--background)) 70%)'
              }}></div>

              {/* Chart Base Circle */}
              <div className="absolute inset-0 flex items-center justify-center">
                <svg className="w-[300px] h-[300px]" viewBox="0 0 300 300">
                  {/* Outer Ring */}
                  <circle cx="150" cy="150" r="140" className="stroke-[hsl(var(--border))/0.2] stroke-1 fill-none" />

                  {/* Zodiac Signs */}
                  {[0,30,60,90,120,150,180,210,240,270,300,330].map((deg, i) => {
                    const sign = ['♈','♉','♊','♋','♌','♍','♎','♏','♐','♑','♒','♓'][i];
                    const angle = (deg * Math.PI) / 180;
                    const x1 = 130 * Math.cos(angle) + 150;
                    const y1 = 130 * Math.sin(angle) + 150;
                    const x2 = 150 * Math.cos(angle) + 150;
                    const y2 = 150 * Math.sin(angle) + 150;
                    return (
                      <text key={i} x={x2} y={y2 + 5} textAnchor="middle" fontSize="14" fill="hsl(var(--foreground-muted))/0.5">
                        {sign}
                      </text>
                    );
                  })}

                  {/* Planets */}
                  {[
                    {planet: '☉', angle: 45, distance: 100},
                    {planet: '☽', angle: 120, distance: 80},
                    {planet: '♃', angle: 210, distance: 90},
                    {planet: '♄', angle: 300, distance: 110},
                    {planet: '♀', angle: 60, distance: 70},
                    {planet: '☿', angle: 30, distance: 60},
                    {planet: '♂', angle: 240, distance: 95}
                  ].map((p, i) => {
                    const angle = (p.angle * Math.PI) / 180;
                    const x = p.distance * Math.cos(angle) + 150;
                    const y = p.distance * Math.sin(angle) + 150;
                    return (
                      <text key={i} x={x} y={y + 5} textAnchor="middle" fontSize="18" fill="hsl(var(--accent))">
                        {p.planet}
                      </text>
                    );
                  })}

                  {/* Center Point */}
                  <circle cx="150" cy="150" r="4" className="fill-[hsl(var(--accent))]" />
                </svg>
              </div>

              {/* Chart Info Overlay */}
              <div className="absolute bottom-4 left-4 right-4 text-center">
                <h3 className="text-lg font-semibold text-[hsl(var(--foreground))]">
                  Sample D1 Chart
                </h3>
                <p className="text-sm text-[hsl(var(--foreground-muted))]">
                  August 15, 1990 • 2:30 PM • Mumbai, IN
                </p>
              </div>
            </div>

            <div className="mt-6 flex justify-center space-x-4">
              <ButtonVariant
                variant="outline"
                size="md"
              >
                <Moon className="h-4 w-4 mr-2" />
                View Sample Chart
              </ButtonVariant>
              <ButtonVariant
                variant="primary"
                size="md"
              >
                <Sparkles className="h-4 w-4 mr-2" />
                Generate My Chart
              </ButtonVariant>
            </div>
          </div>
        </div>
      </section>

      {/* Call to Action */}
      <section className="relative py-20 px-6">
        <div className="relative z-10 max-w-3xl mx-auto text-center space-y-8">
          <h2 className="text-3xl font-bold text-[hsl(var(--foreground))]">
            Ready to Explore Your Destiny?
          </h2>
          <p className="text-[hsl(var(--foreground-muted))] max-w-2xl mx-auto">
            Join thousands of seekers who have discovered profound insights through precise astrological calculations.
          </p>

          <div className="flex flex-col sm:flex-row space-y-4 sm:space-y-0 sm:space-x-4 justify-center">
            <InputGroup>
              <input
                type="text"
                placeholder="Enter your birth date (YYYY-MM-DD)"
                className="flex-1 px-4 py-3 border border-[hsl(var(--border))/0.3] rounded-lg bg-[hsl(var(--background))/0.2] text-[hsl(var(--foreground))] focus:outline-none focus:ring-2 focus:ring-[hsl(var(--accent))] transition-all"
              />
            </InputGroup>
            <ButtonVariant
              variant="primary"
              size="lg"
              className="flex-1"
            >
              <Sparkles className="h-4 w-4 mr-2" />
              Begin Your Journey
            </ButtonVariant>
          </div>

          <div className="text-[hsl(var(--foreground-muted))] text-sm mt-6">
            <Star className="h-4 w-4 inline-block align-middle animate-star-twinkle mr-2" />
            No credit card required • Instant results • Privacy protected
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="relative py-12 px-6 bg-[hsl(var(--background))/0.2] backdrop-blur-sm">
        <div className="relative z-10 max-w-4xl mx-auto text-center space-y-6">
          <div className="flex flex-col sm:flex-row space-y-4 sm:space-y-0 sm:space-x-8 justify-center">
            <a href="#" className="text-[hsl(var(--foreground-muted))] hover:text-[hsl(var(--foreground))] transition-colors">
              About AstroAI
            </a>
            <a href="#" className="text-[hsl(var(--foreground-muted))] hover:text-[hsl(var(--foreground))] transition-colors">
              How It Works
            </a>
            <a href="#" className="text-[hsl(var(--foreground-muted))] hover:text-[hsl(var(--foreground))] transition-colors">
              Blog
            </a>
            <a href="#" className="text-[hsl(var(--foreground-muted))] hover:text-[hsl(var(--foreground))] transition-colors">
              Contact
            </a>
          </div>

          <div className="flex flex-col sm:flex-row space-y-4 sm:space-y-0 sm:space-x-8 justify-center text-[hsl(var(--foreground-muted))]">
            <span>Chart Calculation: Swiss Ephemeris</span>
            <span>Ayanamsa: Lahiri</span>
            <span>House System: Placidus</span>
          </div>

          <p className="text-[hsl(var(--foreground-muted))] text-sm">
            © 2026 AstroAI. All rights reserved.
            <span className="mx-2">•</span>
            For entertainment purposes only.
          </p>
        </div>
      </footer>
    </div>
  );
}

// Component variants
function ButtonVariant({
  variant = 'primary',
  size = 'md',
  children,
  className = ''
}) {
  const baseClasses = "flex items-center justify-center gap-2 font-medium transition-all disabled:opacity-50 disabled:pointer-events-none";

  const variantClasses = {
    primary: "bg-[hsl(var(--accent))] text-[hsl(var(--background))] hover:bg-[hsl(var(--accent-light))]",
    outline: "border border-[hsl(var(--border))/0.3] text-[hsl(var(--foreground))] hover:bg-[hsl(var(--foreground))/0.05]"
  };

  const sizeClasses = {
    sm: "px-4 py-2 text-sm",
    md: "px-6 py-3 text-base",
    lg: "px-8 py-4 text-lg"
  };

  return (
    <button
      className={`${baseClasses} ${variantClasses[variant]} ${sizeClasses[size]} ${className}`}
    >
      {children}
    </button>
  );
}

function FeatureCard({ icon, title, description }) {
  return (
    <div className="glass p-6 rounded-xl border border-[hsl(var(--border))/0.2] backdrop-blur-sm hover:border-[hsl(var(--border))/0.4] transition-all">
      <div className="mb-4">{icon}</div>
      <h3 className="font-semibold text-[hsl(var(--foreground))] mb-2">{title}</h3>
      <p className="text-[hsl(var(--foreground-muted))]">{description}</p>
    </div>
  );
}

function InputGroup({ children, className = '' }) {
  return (
    <div className={`flex items-center space-x-2 ${className}`}>
      {children}
    </div>
  );
}