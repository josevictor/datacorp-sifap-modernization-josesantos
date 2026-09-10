import type { Metadata } from 'next';
import './globals.css';

export const metadata: Metadata = {
  title: 'SIFAP — Consulta de beneficiário',
  description: 'Consulta de cadastro de beneficiário e histórico de pagamentos.',
};

export default function RootLayout({
  children,
}: Readonly<{ children: React.ReactNode }>) {
  return (
    <html lang="pt-BR">
      <body className="min-h-screen bg-slate-50 text-slate-900 antialiased">
        <div className="mx-auto max-w-4xl px-4 py-8">{children}</div>
      </body>
    </html>
  );
}
