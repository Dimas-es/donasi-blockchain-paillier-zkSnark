import { useState } from 'react';
import type { Donation } from '../api/client';
import { Badge, statusTone } from './ui/Badge';
import { Card } from './ui/Card';
import { formatDateTime, statusLabel, truncateMiddle } from '../lib/format';

type Props = {
  donation: Donation;
  campaignTitle?: string;
};

export function VerificationCard({ donation, campaignTitle }: Props) {
  const [copied, setCopied] = useState<string | null>(null);
  const [showFullCipher, setShowFullCipher] = useState(false);

  function copyToClipboard(text: string, label: string) {
    navigator.clipboard.writeText(text);
    setCopied(label);
    setTimeout(() => setCopied(null), 2000);
  }

  const isConfirmed = donation.status === 'confirmed';

  return (
    <Card
      title="Hasil Verifikasi Kriptografi & On-Chain"
      subtitle={`Donation ID: ${donation.id}`}
      action={
        <Badge tone={statusTone(donation.status)}>
          {statusLabel(donation.status)}
        </Badge>
      }
    >
      <div className="verify-card-grid">
        {/* Banner Status */}
        <div
          className={`verify-banner ${
            isConfirmed ? 'verify-banner--success' : 'verify-banner--warning'
          }`}
        >
          <div className="verify-banner__icon" aria-hidden>
            {isConfirmed ? '✓' : 'ℹ'}
          </div>
          <div>
            <strong>
              {isConfirmed
                ? 'Donasi Terverifikasi Sah (Canonical Record)'
                : `Status Transaksi: ${statusLabel(donation.status)}`}
            </strong>
            <p className="small muted" style={{ margin: '0.25rem 0 0' }}>
              {isConfirmed
                ? 'Transaksi tercatat permanen pada ledger EVM, proof zk-SNARK sah, dan ciphertext telah diagregasikan.'
                : 'Transaksi masih dalam proses pipeline atau belum dikonfirmasi oleh node.'}
            </p>
          </div>
        </div>

        {/* Info Meta */}
        <div className="verify-section">
          <h3 className="verify-section__title">1. Informasi Kampanye & Waktu</h3>
          <dl className="verify-dl">
            {campaignTitle ? (
              <div>
                <dt>Nama Kampanye</dt>
                <dd><strong>{campaignTitle}</strong></dd>
              </div>
            ) : null}
            <div>
              <dt>Campaign ID</dt>
              <dd className="mono">{donation.campaign_id}</dd>
            </div>
            <div>
              <dt>Waktu Pencatatan</dt>
              <dd>{formatDateTime(donation.created_at)}</dd>
            </div>
          </dl>
        </div>

        {/* Bukti On-Chain */}
        <div className="verify-section">
          <h3 className="verify-section__title">2. Bukti On-Chain (Blockchain Ledger)</h3>
          <dl className="verify-dl">
            <div>
              <dt>Transaction Hash</dt>
              <dd className="mono">
                {donation.tx_hash ? (
                  <span className="verify-copyable">
                    <span>{truncateMiddle(donation.tx_hash, 16, 12)}</span>
                    <button
                      type="button"
                      className="btn-copy"
                      onClick={() => copyToClipboard(donation.tx_hash, 'tx')}
                    >
                      {copied === 'tx' ? 'Tersalin!' : 'Salin'}
                    </button>
                  </span>
                ) : (
                  <span className="muted">Belum ada tx_hash (tertunda)</span>
                )}
              </dd>
            </div>
            <div>
              <dt>Smart Contract</dt>
              <dd className="mono">DonationRegistry (EVM alt_bn128 Precompiles)</dd>
            </div>
          </dl>
        </div>

        {/* Bukti Zero-Knowledge */}
        <div className="verify-section">
          <h3 className="verify-section__title">3. Bukti Zero-Knowledge (zk-SNARK Groth16)</h3>
          <dl className="verify-dl">
            <div>
              <dt>Poseidon Commitment</dt>
              <dd className="mono">
                <span className="verify-copyable">
                  <span>{truncateMiddle(donation.commitment, 14, 10)}</span>
                  <button
                    type="button"
                    className="btn-copy"
                    onClick={() => copyToClipboard(donation.commitment, 'comm')}
                  >
                    {copied === 'comm' ? 'Tersalin!' : 'Salin'}
                  </button>
                </span>
              </dd>
            </div>
            <div>
              <dt>Sifat Pembuktian</dt>
              <dd>
                <span className="verify-badge-pill">Range Soundness: 0 &lt; amount ≤ max</span>
                <span className="verify-badge-pill">Commitment Hiding &amp; Binding</span>
              </dd>
            </div>
          </dl>
        </div>

        {/* Ciphertext Paillier */}
        <div className="verify-section">
          <h3 className="verify-section__title">4. Ciphertext Paillier (IND-CPA)</h3>
          <p className="small muted">
            Nominal donatur terenkripsi pada grup modulus ring Paillier 2048-bit (c = g^m · r^n mod n²).
          </p>
          <div className="verify-cipher-box">
            <code className="mono small">
              {showFullCipher
                ? donation.encrypted_amount
                : truncateMiddle(donation.encrypted_amount, 24, 20)}
            </code>
            {donation.encrypted_amount.length > 50 ? (
              <button
                type="button"
                className="btn-text small"
                onClick={() => setShowFullCipher(!showFullCipher)}
              >
                {showFullCipher ? 'Tampilkan ringkas' : 'Lihat ciphertext penuh'}
              </button>
            ) : null}
          </div>
        </div>
      </div>
    </Card>
  );
}
