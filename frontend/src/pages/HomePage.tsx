import { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { apiRequest, type Campaign } from '../api/client';
import { CampaignCard } from '../components/CampaignCard';
import { Spinner } from '../components/ui/Spinner';
import { useAuth } from '../context/AuthContext';

export function HomePage() {
  const { user } = useAuth();
  const [campaigns, setCampaigns] = useState<Campaign[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    apiRequest<{ data: Campaign[] }>('/api/campaigns')
      .then((result) => setCampaigns(result.data.slice(0, 6)))
      .catch(() => setCampaigns([]))
      .finally(() => setLoading(false));
  }, []);

  return (
    <div className="home">
      <section className="hero-editorial">
        <div className="hero-editorial__inner">
          <div className="hero-editorial__badges">
            <span className="badge-chip">Blockchain</span>
            <span className="badge-chip">Paillier</span>
            <span className="badge-chip">zk-SNARK</span>
          </div>

          <h1 className="hero-editorial__title">
            Donasi Transparan, Privasi Terlindungi
          </h1>

          <p className="hero-editorial__lead">
            Sistem donasi terverifikasi blockchain dengan enkripsi homomorfik Paillier dan pembuktian zk-SNARK Groth16.
            Nominal donatur tetap rahasia, sementara total agregat dan validitas transaksi dapat diaudit publik secara on-chain.
          </p>

          <div className="hero-editorial__actions">
            <Link to="/campaigns" className="btn-action btn-action--primary">
              Jelajahi Campaign
            </Link>
            <Link to="/verify" className="btn-action btn-action--outline">
              Buka Public Explorer
            </Link>
          </div>
        </div>
      </section>

      <section className="section">
        <header className="section__header">
          <h2>Campaign terbaru</h2>
          <Link to="/campaigns">Lihat semua</Link>
        </header>
        {loading ? (
          <Spinner label="Memuat campaign" />
        ) : campaigns.length === 0 ? (
          <div className="empty-state">
            <h3>Belum ada campaign</h3>
            <p>Login dan buat campaign pertama untuk memulai demo.</p>
            <Link to={user ? '/campaigns/new' : '/login'} className="link-btn link-btn--primary">
              {user ? 'Buat campaign' : 'Masuk'}
            </Link>
          </div>
        ) : (
          <div className="campaign-grid">
            {campaigns.map((campaign) => (
              <CampaignCard key={campaign.id} campaign={campaign} />
            ))}
          </div>
        )}
      </section>
    </div>
  );
}
