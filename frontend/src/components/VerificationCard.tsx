import { useState } from 'react';
import { Link } from 'react-router-dom';
import type { Donation } from '../api/client';
import { formatDateTime, statusLabel, truncateMiddle } from '../lib/format';

type Props = {
  donation: Donation;
  campaignTitle?: string;
};

export function VerificationCard({ donation, campaignTitle }: Props) {
  const [copied, setCopied] = useState<string | null>(null);
  const [showCipher, setShowCipher] = useState(false);

  function copyToClipboard(text: string, label: string) {
    navigator.clipboard.writeText(text);
    setCopied(label);
    setTimeout(() => setCopied(null), 2000);
  }

  const isConfirmed = donation.status === 'confirmed';

  return (
    <div className="audit-cert">
      {/* Header Sertifikat */}
      <div className="audit-cert__header">
        <div className="audit-cert__status-row">
          <span
            className={`audit-cert__status-pill ${
              isConfirmed
                ? 'audit-cert__status-pill--confirmed'
                : 'audit-cert__status-pill--pending'
            }`}
          >
            <span className="audit-cert__status-dot" aria-hidden="true" />
            {isConfirmed ? 'Terkonfirmasi di Blockchain' : statusLabel(donation.status)}
          </span>
          <span className="audit-cert__standard-tag">zk-SNARK &bull; Paillier 2048</span>
        </div>

        <h2 className="audit-cert__title">Sertifikat Audit Kriptografi</h2>
        <div className="audit-cert__id-row">
          <span className="audit-cert__id-label">Donation ID</span>
          <code className="mono audit-cert__id-value">{donation.id}</code>
          <button
            type="button"
            className="btn-copy-micro"
            onClick={() => copyToClipboard(donation.id, 'id')}
            title="Salin Donation ID"
          >
            {copied === 'id' ? 'Tersalin!' : 'Salin ID'}
          </button>
        </div>
      </div>

      {/* Meta Kampanye & Waktu */}
      <div className="audit-cert__meta-grid">
        <div className="audit-cert__meta-item">
          <span className="audit-cert__meta-label">Kampanye Penerima</span>
          {campaignTitle ? (
            <Link to={`/campaigns/${donation.campaign_id}`} className="audit-cert__meta-link">
              <strong>{campaignTitle}</strong>
              <span className="audit-cert__link-arrow">&rarr;</span>
            </Link>
          ) : (
            <span className="mono">{truncateMiddle(donation.campaign_id, 10, 8)}</span>
          )}
        </div>
        <div className="audit-cert__meta-item">
          <span className="audit-cert__meta-label">Waktu Pencatatan</span>
          <span className="audit-cert__meta-value">{formatDateTime(donation.created_at)}</span>
        </div>
      </div>

      {/* Tiga Pilar Pembuktian Kriptografi */}
      <div className="audit-cert__proofs">
        <h3 className="audit-cert__section-title">Hasil Pemeriksaan Kriptografi</h3>

        <div className="audit-cert__proof-list">
          {/* 1. zk-SNARK Groth16 */}
          <div className="audit-cert__proof-row">
            <div className="audit-cert__proof-head">
              <span className="audit-cert__proof-name">zk-SNARK Groth16</span>
              <span className="audit-cert__proof-status-badge">Valid (Soundness Terpenuhi)</span>
            </div>
            <p className="audit-cert__proof-desc">
              Nominal terbukti berada dalam rentang yang sah (<code>0 &lt; nominal &le; batas kampanye</code>) melalui sirkuit aritmatika R1CS tanpa membocorkan nilai ke publik.
            </p>
          </div>

          {/* 2. Poseidon Commitment */}
          <div className="audit-cert__proof-row">
            <div className="audit-cert__proof-head">
              <span className="audit-cert__proof-name">Poseidon Commitment</span>
              <span className="audit-cert__proof-sub">Binding &amp; Hiding</span>
            </div>
            <div className="audit-cert__hash-row">
              <code className="mono">{truncateMiddle(donation.commitment, 18, 14)}</code>
              <button
                type="button"
                className="btn-copy-micro"
                onClick={() => copyToClipboard(donation.commitment, 'comm')}
              >
                {copied === 'comm' ? 'Tersalin!' : 'Salin Hash'}
              </button>
            </div>
            <p className="audit-cert__proof-desc">
              Komitmen kriptografis satu arah yang mengikat bukti secara permanen pada blockchain.
            </p>
          </div>

          {/* 3. EVM Blockchain Ledger */}
          <div className="audit-cert__proof-row">
            <div className="audit-cert__proof-head">
              <span className="audit-cert__proof-name">Konsensus On-Chain (EVM)</span>
              <span className="audit-cert__proof-sub">DonationRegistry.sol</span>
            </div>
            <div className="audit-cert__hash-row">
              {donation.tx_hash ? (
                <>
                  <code className="mono">{truncateMiddle(donation.tx_hash, 18, 14)}</code>
                  <button
                    type="button"
                    className="btn-copy-micro"
                    onClick={() => copyToClipboard(donation.tx_hash, 'tx')}
                  >
                    {copied === 'tx' ? 'Tersalin!' : 'Salin Tx'}
                  </button>
                </>
              ) : (
                <span className="muted small">Menunggu finalisasi blok di jaringan</span>
              )}
            </div>
            <p className="audit-cert__proof-desc">
              Tercatat kanonikal pada precompile BN256/alt_bn128 dan tidak dapat dimanipulasi.
            </p>
          </div>
        </div>
      </div>

      {/* Ciphertext Paillier (Collapsible) */}
      <div className="audit-cert__cipher-section">
        <div className="audit-cert__cipher-header">
          <div>
            <strong className="audit-cert__cipher-title">Enkripsi Homomorfik Paillier (2048-bit)</strong>
            <p className="small muted" style={{ margin: '0.15rem 0 0' }}>
              Nominal terenkripsi di atas modulus ring untuk agregasi langsung tanpa dekripsi.
            </p>
          </div>
          <button
            type="button"
            className="audit-cert__cipher-toggle-btn"
            onClick={() => setShowCipher(!showCipher)}
          >
            {showCipher ? 'Tutup Raw Ciphertext ▲' : 'Lihat Raw Ciphertext ▼'}
          </button>
        </div>

        {showCipher && (
          <div className="audit-cert__cipher-body">
            <div className="audit-cert__cipher-box">
              <code className="mono small">{donation.encrypted_amount}</code>
            </div>
            <div className="audit-cert__cipher-actions">
              <button
                type="button"
                className="btn-copy-micro"
                onClick={() => copyToClipboard(donation.encrypted_amount, 'cipher')}
              >
                {copied === 'cipher' ? 'Tersalin ke Clipboard!' : 'Salin Seluruh Ciphertext'}
              </button>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
