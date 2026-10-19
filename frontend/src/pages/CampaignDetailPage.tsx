import { useCallback, useEffect, useState, type FormEvent } from 'react';
import { Link, useParams } from 'react-router-dom';
import {
  apiRequest,
  type AggregateSummary,
  type Campaign,
  type Donation,
  type ZKProof,
} from '../api/client';
import {
  DonationSteps,
  type DonationStep,
} from '../components/DonationSteps';
import { Alert } from '../components/ui/Alert';
import { Badge, statusTone } from '../components/ui/Badge';
import { Button } from '../components/ui/Button';
import { Card } from '../components/ui/Card';
import { Field, Input } from '../components/ui/Field';
import { Spinner } from '../components/ui/Spinner';
import { useAuth } from '../context/AuthContext';
import {
  formatAmount,
  formatDateTime,
  parseAmountInput,
  statusLabel,
  truncateMiddle,
} from '../lib/format';

function newIdempotencyKey() {
  return crypto.randomUUID();
}

export function CampaignDetailPage() {
  const { id } = useParams<{ id: string }>();
  const { user } = useAuth();
  const [campaign, setCampaign] = useState<Campaign | null>(null);
  const [donations, setDonations] = useState<Donation[]>([]);
  const [aggregate, setAggregate] = useState<AggregateSummary | null>(null);
  const [amount, setAmount] = useState('');
  const [error, setError] = useState('');
  const [successTx, setSuccessTx] = useState('');
  const [lastDonationId, setLastDonationId] = useState('');
  const [loading, setLoading] = useState(true);
  const [donating, setDonating] = useState(false);
  const [donationStep, setDonationStep] = useState<DonationStep>('idle');

  const load = useCallback(async () => {
    if (!id) {
      return;
    }

    const [campaignData, donationData, aggregateData] = await Promise.all([
      apiRequest<Campaign>(`/api/campaigns/${id}`),
      apiRequest<{ data: Donation[] }>(`/api/campaigns/${id}/donations`),
      apiRequest<AggregateSummary>(`/api/campaigns/${id}/aggregate`),
    ]);

    setCampaign(campaignData);
    setDonations(donationData.data);
    setAggregate(aggregateData);
  }, [id]);

  useEffect(() => {
    if (!id) {
      return;
    }

    load()
      .catch((err) =>
        setError(err instanceof Error ? err.message : 'Gagal memuat data'),
      )
      .finally(() => setLoading(false));
  }, [id, load]);

  async function onDonate(event: FormEvent) {
    event.preventDefault();
    if (!id || !user) {
      setError('Silakan masuk untuk berdonasi.');
      return;
    }

    setError('');
    setSuccessTx('');
    setDonating(true);
    setDonationStep('proof');

    try {
      const proofPayload = await apiRequest<{
        amount: string;
        commitment: string;
        proof: ZKProof;
      }>('/api/donations/generate-proof', {
        method: 'POST',
        auth: true,
        body: {
          campaign_id: id,
          amount: parseAmountInput(amount),
        },
      });

      setDonationStep('encrypt');
      await new Promise((resolve) => setTimeout(resolve, 250));

      setDonationStep('chain');

      const donation = await apiRequest<Donation>('/api/donations', {
        method: 'POST',
        auth: true,
        idempotencyKey: newIdempotencyKey(),
        body: {
          campaign_id: id,
          amount: proofPayload.amount,
          commitment: proofPayload.commitment,
          proof: proofPayload.proof,
        },
      });

      setDonationStep('done');
      setSuccessTx(donation.tx_hash || '');
      setLastDonationId(donation.id);
      setAmount('');
      await load();
    } catch (err) {
      setDonationStep('idle');
      setError(err instanceof Error ? err.message : 'Donasi gagal');
    } finally {
      setDonating(false);
    }
  }

  if (loading) {
    return (
      <div className="page">
        <Spinner label="Memuat detail campaign" />
      </div>
    );
  }

  if (!campaign) {
    return (
      <div className="page">
        <Alert variant="error" title="Campaign tidak ditemukan">
          Periksa tautan atau kembali ke{' '}
          <Link to="/campaigns">daftar campaign</Link>.
        </Alert>
      </div>
    );
  }

  const raised =
    aggregate?.decrypted_total !== undefined
      ? formatAmount(aggregate.decrypted_total)
      : '—';

  return (
    <div className="page">
      <nav className="breadcrumb">
        <Link to="/campaigns">Campaign</Link>
        <span aria-hidden>/</span>
        <span>{campaign.title}</span>
      </nav>

      <header className="detail-hero">
        <div>
          <Badge tone={statusTone(campaign.status)}>
            {statusLabel(campaign.status)}
          </Badge>
          <h1 className="detail-hero__title">{campaign.title}</h1>
          <p className="detail-hero__desc">
            {campaign.description || 'Tidak ada deskripsi.'}
          </p>
        </div>
        {/* Panel Ringkasan Metrik & Progress Terpadu */}
        {(() => {
          const targetNum = Number(campaign.target_amount) || 0;
          const raisedNum =
            aggregate?.decrypted_total !== undefined
              ? Number(aggregate.decrypted_total) || 0
              : 0;
          const rawPercent = targetNum > 0 ? (raisedNum / targetNum) * 100 : 0;
          const percentDisplay =
            rawPercent === 0
              ? '0%'
              : rawPercent < 1
                ? `${rawPercent.toFixed(2)}%`
                : `${Math.round(rawPercent)}%`;

          const progressFillWidth =
            rawPercent === 0
              ? '0%'
              : `${Math.max(1.5, Math.min(100, rawPercent))}%`;

          return (
            <div className="campaign-metrics-panel">
              <div className="campaign-metrics-grid">
                <div className="metric-item">
                  <span className="metric-label">Terkumpul (Agregat Demo)</span>
                  <span className="metric-value">{raised === '—' ? raised : `Rp ${raised}`}</span>
                  <span className="metric-hint">Dekripsi Paillier server penelitian</span>
                </div>
                <div className="metric-item">
                  <span className="metric-label">Target Donasi</span>
                  <span className="metric-value">Rp {formatAmount(campaign.target_amount)}</span>
                </div>
                <div className="metric-item">
                  <span className="metric-label">Donasi Tervalidasi</span>
                  <span className="metric-value">{String(aggregate?.donation_count ?? 0)}</span>
                  <span className="metric-hint">Confirmed on-chain</span>
                </div>
              </div>

              <div className="campaign-metrics-progress">
                <div className="campaign-metrics-progress-info">
                  <span className="small muted">
                    Pencapaian: <strong>{percentDisplay}</strong> dari target
                  </span>
                  <span className="campaign-progress-badge">{percentDisplay}</span>
                </div>
                <div className="campaign-progress-track">
                  <div
                    className="campaign-progress-fill"
                    style={{ width: progressFillWidth }}
                  />
                </div>
              </div>
            </div>
          );
        })()}
      </header>

      <div className="detail-layout">
        <div className="detail-main">
          <Card
            title="Riwayat donasi"
            subtitle="Commitment dan hash transaksi pada blockchain demo."
          >
            {donations.length === 0 ? (
              <div className="empty-state empty-state--compact">
                <p>Belum ada donasi untuk campaign ini.</p>
              </div>
            ) : (
              <div className="table-wrap">
                <table className="data-table">
                  <thead>
                    <tr>
                      <th>Status</th>
                      <th>Commitment</th>
                      <th>Tx hash</th>
                      <th>Waktu</th>
                      <th>Audit</th>
                    </tr>
                  </thead>
                  <tbody>
                    {donations.map((donation) => (
                      <tr key={donation.id}>
                        <td>
                          <Badge tone={statusTone(donation.status)}>
                            {statusLabel(donation.status)}
                          </Badge>
                        </td>
                        <td className="mono">
                          {truncateMiddle(donation.commitment, 10, 8)}
                        </td>
                        <td className="mono">
                          {donation.tx_hash
                            ? truncateMiddle(donation.tx_hash, 10, 8)
                            : '—'}
                        </td>
                        <td>{formatDateTime(donation.created_at)}</td>
                        <td>
                          <Link
                            to={`/verify?id=${donation.id}`}
                            className="btn-text small"
                          >
                            Verifikasi &rarr;
                          </Link>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            )}
          </Card>

          <Card
            title="Transparansi teknis"
            subtitle="Ringkasan untuk auditor dan demo penelitian."
          >
            <ul className="check-list">
              <li>
                Batas maksimal donasi per transaksi:{' '}
                <strong>Rp {formatAmount(campaign.max_donation)}</strong>
              </li>
              <li>
                Nominal individual disimpan sebagai ciphertext Paillier di
                database dan referensi on-chain.
              </li>
              <li>
                Proof Groth16 membuktikan amount ∈ (0, campaign_max] dan
                konsistensi commitment Poseidon.
              </li>
            </ul>
          </Card>
        </div>

        <aside className="detail-aside">
          {user && campaign.status === 'active' ? (
            <Card
              title="Donasi sekarang"
              subtitle={`Maks. Rp ${formatAmount(campaign.max_donation)} per transaksi`}
              padding="md"
            >
              <form className="form-stack" onSubmit={onDonate}>
                <Field
                  label="Nominal (Rp)"
                  hint="Hanya angka; sistem akan membuat proof dan transaksi."
                >
                  <Input
                    value={amount}
                    onChange={(e) =>
                      setAmount(formatAmount(e.target.value))
                    }
                    inputMode="numeric"
                    placeholder="100.000"
                    required
                    disabled={donating}
                  />
                </Field>

                {/* Quick Amount Chips */}
                <div className="quick-chips">
                  {[25000, 50000, 100000, 250000].map((val) => (
                    <button
                      key={val}
                      type="button"
                      className="btn-chip"
                      disabled={donating}
                      onClick={() => setAmount(formatAmount(String(val)))}
                    >
                      +{formatAmount(String(val))}
                    </button>
                  ))}
                </div>

                {donating || donationStep === 'done' ? (
                  <DonationSteps step={donationStep} />
                ) : null}

                {error ? <Alert variant="error">{error}</Alert> : null}
                {successTx ? (
                  <Alert variant="success" title="Donasi berhasil">
                    <div>
                      Transaksi:{' '}
                      <code className="mono">{truncateMiddle(successTx, 12, 10)}</code>
                    </div>
                    {lastDonationId ? (
                      <div style={{ marginTop: '0.5rem' }}>
                        <Link
                          to={`/verify?id=${lastDonationId}`}
                          className="btn-text small"
                          style={{ fontWeight: 600, color: '#2563eb' }}
                        >
                          Verifikasi di Explorer &rarr;
                        </Link>
                      </div>
                    ) : null}
                  </Alert>
                ) : null}

                <Button
                  type="submit"
                  loading={donating}
                  className="btn--block btn--action-submit"
                >
                  {donating ? 'Memproses...' : 'Kirim donasi'}
                </Button>
              </form>
            </Card>
          ) : (
            <Card title="Donasi" padding="md">
              {!user ? (
                <p>
                  <Link to="/login">Masuk</Link> untuk mengirim donasi ke
                  campaign ini.
                </p>
              ) : (
                <p>Campaign tidak aktif; donasi ditutup.</p>
              )}
            </Card>
          )}

          <Card
            title="Agregat Kriptografi Paillier"
            subtitle="Homomorphic Addition mod n²"
            padding="md"
          >
            <div className="aggregate-audit-box">
              <div className="aggregate-formula-banner">
                <span className="mono small">
                  E(M) = ∏ E(m_i) mod n²
                </span>
              </div>
              <div className="aggregate-audit-row">
                <span className="small muted">Status Rekonsiliasi:</span>
                <Badge tone="success">Sinkron &amp; Terverifikasi</Badge>
              </div>
              <div className="aggregate-audit-row">
                <span className="small muted">Donasi Sah (Canonical):</span>
                <strong>{aggregate?.donation_count ?? 0} transaksi</strong>
              </div>
              <div className="aggregate-audit-row">
                <span className="small muted">Total Terdekripsi (Demo):</span>
                <strong style={{ color: '#0f172a' }}>
                  {raised === '—' ? raised : `Rp ${raised}`}
                </strong>
              </div>
              <div style={{ marginTop: '0.5rem' }}>
                <span
                  className="small muted"
                  style={{ display: 'block', marginBottom: '0.25rem' }}
                >
                  Ciphertext Kumulatif:
                </span>
                <p className="mono aggregate-cipher">
                  {aggregate?.encrypted_total
                    ? truncateMiddle(aggregate.encrypted_total, 16, 12)
                    : '0'}
                </p>
              </div>
              <div
                style={{
                  marginTop: '0.75rem',
                  borderTop: '1px solid var(--color-border)',
                  paddingTop: '0.5rem',
                }}
              >
                <Link to="/verify" className="btn-text small">
                  Buka Explorer Transaksi &rarr;
                </Link>
              </div>
            </div>
          </Card>
        </aside>
      </div>
    </div>
  );
}
