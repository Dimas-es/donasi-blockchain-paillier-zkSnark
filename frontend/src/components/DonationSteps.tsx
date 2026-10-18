type Step = 'idle' | 'proof' | 'encrypt' | 'chain' | 'done';

const labels: Record<Step, string> = {
  idle: 'Siap',
  proof: 'Bukti ZK (Groth16)',
  encrypt: 'Enkripsi Paillier (2048-bit)',
  chain: 'Mencatat ke Ledger EVM',
  done: 'Terkonfirmasi & Teragregasi',
};

export function DonationSteps({ step }: { step: Step }) {
  const order: Step[] = ['proof', 'encrypt', 'chain', 'done'];
  const activeIndex =
    step === 'idle' ? -1 : order.indexOf(step === 'done' ? 'done' : step);

  return (
    <ol className="steps" aria-label="Progres donasi">
      {order.map((item, index) => {
        const state =
          activeIndex > index
            ? 'done'
            : activeIndex === index
              ? 'active'
              : 'pending';
        return (
          <li key={item} className={`steps__item steps__item--${state}`}>
            <span className="steps__dot" aria-hidden />
            <span className="steps__label">{labels[item]}</span>
          </li>
        );
      })}
    </ol>
  );
}

export type DonationStep = Step;
