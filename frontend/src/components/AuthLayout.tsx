import { Link } from 'react-router-dom';

export function AuthLayout({
  title,
  subtitle,
  children,
  footer,
}: {
  title: string;
  subtitle: string;
  children: React.ReactNode;
  footer?: React.ReactNode;
}) {
  return (
    <div className="auth-page">
      <div className="auth-card-split">
        {/* Sisi Kiri (60%): Visual, Branding & Kontur Gelombang */}
        <section className="auth-split__left" aria-label="Informasi Platform">
          <div className="auth-split__waves" aria-hidden="true">
            <svg
              className="auth-waves-svg"
              viewBox="0 0 600 700"
              fill="none"
              xmlns="http://www.w3.org/2000/svg"
              preserveAspectRatio="none"
            >
              <path
                d="M-50 140 C 140 90, 260 230, 440 160 C 540 120, 640 200, 750 160"
                stroke="rgba(255,255,255,0.14)"
                strokeWidth="2.5"
              />
              <path
                d="M-80 220 C 120 170, 270 310, 470 240 C 570 200, 670 280, 780 240"
                stroke="rgba(255,255,255,0.16)"
                strokeWidth="2.5"
              />
              <path
                d="M-60 300 C 130 250, 290 390, 490 320 C 590 280, 690 360, 800 320"
                stroke="rgba(255,255,255,0.14)"
                strokeWidth="2.5"
              />
              <path
                d="M-100 380 C 110 330, 260 470, 460 400 C 560 360, 660 440, 760 400"
                stroke="rgba(255,255,255,0.11)"
                strokeWidth="2.5"
              />
              <path
                d="M-40 460 C 150 410, 310 550, 510 480 C 610 440, 710 520, 820 480"
                stroke="rgba(255,255,255,0.08)"
                strokeWidth="2.5"
              />
              <path
                d="M-70 540 C 120 490, 280 630, 480 560 C 580 520, 680 600, 790 560"
                stroke="rgba(255,255,255,0.06)"
                strokeWidth="2.5"
              />
              <path
                d="M-50 60 C 170 20, 230 160, 430 80 C 530 40, 630 120, 740 80"
                stroke="rgba(255,255,255,0.12)"
                strokeWidth="2"
              />
            </svg>
          </div>

          <div className="auth-split__left-inner">
            <div className="auth-split__brand">
              <span className="auth-split__brand-title">TRUSTGIVE</span>
            </div>

            <div className="auth-split__hero">
              <h2 className="auth-split__headline">
                Donasi Transparan, Privasi Terlindungi
              </h2>
              <p className="auth-split__description">
                Sistem donasi terverifikasi blockchain dengan enkripsi homomorfik Paillier dan pembuktian zk-SNARK Groth16.
              </p>
            </div>

            <div className="auth-split__badges">
              <span className="auth-pill">Blockchain</span>
              <span className="auth-pill">Paillier</span>
              <span className="auth-pill">zk-SNARK</span>
            </div>
          </div>
        </section>

        {/* Sisi Kanan (40%): Form Masuk & Navigasi */}
        <section className="auth-split__right" aria-label="Form Masuk">
          <div className="auth-split__top-bar">
            <Link to="/" className="auth-back-link">
              <span aria-hidden="true">&larr;</span> Kembali ke Beranda
            </Link>
          </div>

          <div className="auth-split__form-wrap">
            <header className="auth-form__header">
              <h1 className="auth-form__title">{title}</h1>
              <p className="auth-form__subtitle">{subtitle}</p>
            </header>

            <div className="auth-form__body">{children}</div>

            {footer ? <footer className="auth-form__footer">{footer}</footer> : null}
          </div>
        </section>
      </div>
    </div>
  );
}
