import './globals.css';
import type { Metadata } from 'next';
import { Inter } from 'next/font/google';
import { framerMotion } from '@/lib/utils/framerMotion';

const inter = Inter({ subsets: ['latin'] });

export const metadata: Metadata = {
  title: 'AstroAI - Premium Astrology Platform',
  description: 'Futuristic astrology platform with deterministic chart calculations',
  icons: {
    icon: '/favicon.ico',
  },
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" className="scroll-smooth">
      <body className={framerMotion.bodyInitial}>
        {children}
      </body>
    </html>
  );
}