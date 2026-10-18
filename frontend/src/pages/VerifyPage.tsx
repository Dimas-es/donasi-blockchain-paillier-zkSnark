import { useEffect, useState, type FormEvent } from 'react';
import { Link, useSearchParams } from 'react-router-dom';
import {
  apiRequest,
  type Campaign,
  type Donation,
} from '../api/client';
import { VerificationCard } from '../components/VerificationCard';
import { Alert } from '../components/ui/Alert';
import { Badge, statusTone } from '../components/ui/Badge';
import { Button } from '../components/ui/Button';
import { Card } from '../components/ui/Card';
import { Field, Input } from '../components/ui/Field';
import { Spinner } from '../components/ui/Spinner';
import { formatDateTime, statusLabel, truncateMiddle } from '../lib/format';

export function VerifyPage() {
  const [searchParams, setSearchParams] = useSearchParams();
  const [query, setQuery] = useState(searchParams.get('id') || '');
  const [donation, setDonation] = useState<Donation | null>(null);
  const [campaign, setCampaign] = useState<Campaign | null>(null);
  const [recentDonations, setRecentDonations] = useState<
    (Donation & { campaign_title?: string })[]
  >([]);
  const [loading, setLoading] = useState(false);
  const [loadingRecents, setLoadingRecents] = useState(true);
  const [error, setError] = useState('');

  // 1. Load recent transactions from all active campaigns
  useEffect(() => {
    async function loadExplorerFeed() {
      try {
        const campaignsRes = await apiRequest<{ data: Campaign[] }>('/api/campaigns');
        const campaignsList = campaignsRes.data || [];
        const campMap = new Map<string, string>();
        campaignsList.forEach((c) => campMap.set(c.id, c.title));

        // Fetch donations for first 5 campaigns
        const donationPromises = campaignsList.slice(0, 5).map(async (c) => {
          try {
            const res = await apiRequest<{ data: Donation[] }>(
              `/api/campaigns/${c.id}/donations`,
            );
            return (res.data || []).map((d) => ({
              ...d,
              campaign_title: c.title,
            }));
          } catch {
            return [];
          }
        });

        const nested = await Promise.all(donationPromises);
        const allDonations = nested
          .flat()
          .sort(
            (a, b) =>
              new Date(b.created_at).getTime() - new Date(a.created_at).getTime(),
          );

        setRecentDonations(allDonations.slice(0, 15));
      } catch (err) {
        console.error('Failed to load explorer feed:', err);
      } finally {
        setLoadingRecents(false);
      }
    }

    loadExplorerFeed();
  }, []);

  // 2. Perform verification search by ID, Commitment, or TxHash
  async function performLookup(searchVal: string) {
    const val = searchVal.trim();
    if (!val) return;

    setError('');
    setLoading(true);
    setDonation(null);
    setCampaign(null);

    try {
      // Step A: Attempt direct UUID lookup
      const isUUID =
        /^[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$/i.test(
          val,
        );

      let foundDonation: Donation | null = null;

      if (isUUID) {
        try {
          foundDonation = await apiRequest<Donation>(`/api/donations/${val}`);
        } catch {
          // If not found directly, continue searching
        }
      }

      // Step B: If not found, scan recent / campaign donations
      if (!foundDonation) {
        // Match from recent list first
        const match = recentDonations.find(
          (d) =>
            d.id === val ||
            d.commitment.toLowerCase() === val.toLowerCase() ||
            d.tx_hash.toLowerCase() === val.toLowerCase(),
        );

        if (match) {
          foundDonation = match;
        } else {
          // Deep search across campaigns
          const campaignsRes = await apiRequest<{ data: Campaign[] }>('/api/campaigns');
          for (const c of campaignsRes.data) {
            try {
              const dRes = await apiRequest<{ data: Donation[] }>(
                `/api/campaigns/${c.id}/donations`,
              );
              const m = (dRes.data || []).find(
                (d) =>
                  d.id === val ||
                  d.commitment.toLowerCase() === val.toLowerCase() ||
                  d.tx_hash.toLowerCase() === val.toLowerCase(),
              );
              if (m) {
                foundDonation = m;
                break;
              }
            } catch {
              // ignore
            }
          }
        }
      }

      if (!foundDonation) {
        throw new Error(
          'Donasi tidak ditemukan. Pastikan ID donasi, Commitment, atau Tx Hash sudah benar.',
        );
      }

      setDonation(foundDonation);

      // Load campaign title
      try {
        const camp = await apiRequest<Campaign>(
          `/api/campaigns/${foundDonation.campaign_id}`,
        );
        setCampaign(camp);
      } catch {
        // ignore
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Verifikasi gagal');
    } finally {
      setLoading(false);
    }
  }

  // Handle URL param lookup on mount
  useEffect(() => {
    const initialId = searchParams.get('id');
    if (initialId) {
      setQuery(initialId);
      performLookup(initialId);
    }
  }, [searchParams]);

  function onSearch(e: FormEvent) {
    e.preventDefault();
    if (query) {
      setSearchParams({ id: query });
      performLookup(query);
    }
  }

  function selectDonation(d: Donation) {
    setQuery(d.id);
    setSearchParams({ id: d.id });
    setDonation(d);
    window.scrollTo({ top: 0, behavior: 'smooth' });
  }

  return (
    <div className="page">
      <header className="page-header">
        <h1 className="page-header__title">Explorer &amp; Verifikasi Publik</h1>
        <p className="page-header__subtitle">
          Periksa keabsahan bukti zk-SNARK, status transaksi on-chain, dan ciphertext Paillier secara independen.
        </p>
      </header>

      {/* Form Pencarian */}
      <Card
        title="Cari Bukti Donasi"
        subtitle="Masukkan Donation ID (UUID), Tx Hash (0x...), atau Poseidon Commitment"
        className="verify-search-card"
      >
        <form onSubmit={onSearch} className="verify-search-form">
          <Field label="Identifier Donasi">
            <Input
              type="text"
              placeholder="Contoh: 0x4b78c92a... atau c1f24d77-6229-..."
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              required
            />
          </Field>
          <Button type="submit" loading={loading} className="verify-search-btn">
            {loading ? 'Memverifikasi...' : 'Verifikasi'}
          </Button>
        </form>

        {error ? (
          <div style={{ marginTop: '1rem' }}>
            <Alert variant="error" title="Hasil Verifikasi">
              {error}
            </Alert>
          </div>
        ) : null}
      </Card>

      {/* Tampilan Hasil Verifikasi */}
      {loading ? (
        <div style={{ padding: '2rem 0' }}>
          <Spinner label="Memeriksa bukti kriptografi & ledger..." />
        </div>
      ) : donation ? (
        <div style={{ margin: '1.5rem 0' }}>
          <VerificationCard donation={donation} campaignTitle={campaign?.title} />
        </div>
      ) : null}

      {/* Explorer Feed: Daftar Donasi Terbaru */}
      <section className="section" style={{ marginTop: '2.5rem' }}>
        <header className="section__header">
          <div>
            <h2>Live Transaction Feed</h2>
            <p className="muted small">
              Transaksi donasi terbaru yang tercatat di jaringan blockchain dan database penelitian.
            </p>
          </div>
        </header>

        {loadingRecents ? (
          <Spinner label="Memuat transaksi terbaru..." />
        ) : recentDonations.length === 0 ? (
          <div className="empty-state empty-state--compact">
            <p>Belum ada transaksi donasi yang tercatat.</p>
          </div>
        ) : (
          <div className="table-wrap">
            <table className="data-table">
              <thead>
                <tr>
                  <th>Status</th>
                  <th>Kampanye</th>
                  <th>Commitment</th>
                  <th>Tx Hash</th>
                  <th>Waktu</th>
                  <th>Aksi</th>
                </tr>
              </thead>
              <tbody>
                {recentDonations.map((d) => (
                  <tr key={d.id}>
                    <td>
                      <Badge tone={statusTone(d.status)}>
                        {statusLabel(d.status)}
                      </Badge>
                    </td>
                    <td>
                      {d.campaign_title ? (
                        <Link
                          to={`/campaigns/${d.campaign_id}`}
                          className="link-subtle"
                        >
                          <strong>{d.campaign_title}</strong>
                        </Link>
                      ) : (
                        <span className="mono">{truncateMiddle(d.campaign_id, 8, 6)}</span>
                      )}
                    </td>
                    <td className="mono">{truncateMiddle(d.commitment, 10, 8)}</td>
                    <td className="mono">
                      {d.tx_hash ? truncateMiddle(d.tx_hash, 10, 8) : '—'}
                    </td>
                    <td>{formatDateTime(d.created_at)}</td>
                    <td>
                      <button
                        type="button"
                        className="btn-text small"
                        onClick={() => selectDonation(d)}
                      >
                        Inspeksi &rarr;
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </section>

      {/* Penjelasan Transparansi Kriptografi */}
      <Card
        title="Bagaimana Privasi dan Verifikasi Bekerja?"
        subtitle="Prinsip dasar keterbukaan tanpa mengorbankan privasi donatur"
        className="verify-explainer"
      >
        <div className="verify-explainer-grid">
          <div>
            <h4>1. zk-SNARK Groth16</h4>
            <p className="small muted">
              Membuktikan secara matematis bahwa nilai donasi berada di dalam rentang yang sah (0 &lt; amount &le; campaign_max) tanpa mempublikasikan nominal angka tersebut ke publik.
            </p>
          </div>
          <div>
            <h4>2. Enkripsi Homomorfik Paillier</h4>
            <p className="small muted">
              Nominal disimpan dalam bentuk ciphertext di atas modulus ring 2048-bit. Penjumlahan dana dilakukan langsung di atas ciphertext tanpa perlu didekripsi.
            </p>
          </div>
          <div>
            <h4>3. Audit On-Chain Tanpa Bocor</h4>
            <p className="small muted">
              Setiap orang dapat memeriksa bahwa hash transaksi tercatat di blockchain dan bukti ZK sah, namun tidak seorang pun selain donatur yang mengetahui besaran uang yang dikirim.
            </p>
          </div>
        </div>
      </Card>
    </div>
  );
}
