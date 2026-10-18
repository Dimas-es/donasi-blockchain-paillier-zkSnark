import { useState, type FormEvent } from 'react';
import { useNavigate } from 'react-router-dom';
import { AuthLayout } from '../components/AuthLayout';
import { Alert } from '../components/ui/Alert';
import { Button } from '../components/ui/Button';
import { Field, Input } from '../components/ui/Field';
import { useAuth } from '../context/AuthContext';

export function LoginPage() {
  const { login } = useAuth();
  const navigate = useNavigate();
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  async function onSubmit(event: FormEvent) {
    event.preventDefault();
    setError('');
    setLoading(true);

    try {
      await login(email, password);
      navigate('/campaigns');
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Login gagal');
    } finally {
      setLoading(false);
    }
  }

  return (
    <AuthLayout
      title="Masuk ke Sistem"
      subtitle="Akses akun pengujian dan pengelolaan donasi."
      footer={
        <p className="auth-footer-text">
          Platform ini dikembangkan khusus untuk keperluan riset akademik dan pengujian keamanan privasi donatur.
        </p>
      }
    >
      <form className="form-stack" onSubmit={onSubmit}>
        <Field label="Alamat Email">
          <Input
            type="email"
            autoComplete="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            placeholder="pengelola@demo.local"
            required
          />
        </Field>
        <Field label="Kata Sandi">
          <Input
            type="password"
            autoComplete="current-password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            placeholder="••••••••"
            required
          />
        </Field>

        {error ? <Alert variant="error">{error}</Alert> : null}

        <Button
          type="submit"
          loading={loading}
          className="btn--block btn--auth-submit"
          style={{ marginTop: '1rem' }}
        >
          {loading ? 'Memverifikasi...' : 'Masuk'}
        </Button>
      </form>
    </AuthLayout>
  );
}
