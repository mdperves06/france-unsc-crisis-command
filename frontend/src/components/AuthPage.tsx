import React, { useState } from 'react';
import { authLogin, authRegister } from '../lib/api';

interface AuthPageProps {
  onAuthenticated: (user: any) => void;
}

const COUNTRIES = [
  'France', 'United States', 'United Kingdom', 'China', 'Russia',
  'Germany', 'Japan', 'India', 'Brazil', 'South Africa',
  'Egypt', 'UAE', 'Turkey', 'Pakistan', 'Iran',
];

export function AuthPage({ onAuthenticated }: AuthPageProps) {
  const [mode, setMode] = useState<'login' | 'register'>('login');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  // Login state
  const [loginEmail, setLoginEmail] = useState('');
  const [loginPassword, setLoginPassword] = useState('');

  // Register state
  const [regEmail, setRegEmail] = useState('');
  const [regUsername, setRegUsername] = useState('');
  const [regFullName, setRegFullName] = useState('');
  const [regPassword, setRegPassword] = useState('');
  const [regCountry, setRegCountry] = useState('France');

  async function handleLogin(e: React.FormEvent) {
    e.preventDefault();
    setLoading(true);
    setError('');
    try {
      const data = await authLogin(loginEmail, loginPassword);
      onAuthenticated(data.user);
    } catch (err: any) {
      setError(err.message || 'Login failed');
    } finally {
      setLoading(false);
    }
  }

  async function handleRegister(e: React.FormEvent) {
    e.preventDefault();
    setLoading(true);
    setError('');
    try {
      const data = await authRegister({
        email: regEmail,
        username: regUsername,
        full_name: regFullName,
        password: regPassword,
        country_assignment: regCountry,
      });
      onAuthenticated(data.user);
    } catch (err: any) {
      setError(err.message || 'Registration failed');
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="min-h-screen bg-[#050814] flex items-center justify-center px-4 relative overflow-hidden">
      {/* Animated background grid */}
      <div className="absolute inset-0 tactical-grid opacity-30" />

      {/* Glow orbs */}
      <div className="absolute top-1/4 left-1/4 w-96 h-96 bg-blue-600/10 rounded-full blur-3xl animate-pulse" />
      <div className="absolute bottom-1/4 right-1/4 w-80 h-80 bg-cyan-500/8 rounded-full blur-3xl animate-pulse" style={{ animationDelay: '1.5s' }} />

      <div className="relative z-10 w-full max-w-md">
        {/* Logo / Header */}
        <div className="text-center mb-8">
          <div className="inline-flex items-center justify-center w-16 h-16 bg-gradient-to-br from-blue-600 to-cyan-500 rounded-xl mb-4 shadow-lg shadow-blue-500/30">
            <span className="text-2xl">🇫🇷</span>
          </div>
          <h1 className="text-2xl font-bold text-white tracking-wide font-mono">
            FRANCE UNSC<br />
            <span className="text-cyan-400">CRISIS COMMAND</span>
          </h1>
          <p className="text-slate-500 text-xs mt-2 font-mono tracking-widest uppercase">
            Permanent Mission · United Nations
          </p>
        </div>

        {/* Card */}
        <div className="bg-slate-900/80 backdrop-blur-xl border border-slate-700/50 rounded-2xl p-8 shadow-2xl">
          {/* Tab Toggle */}
          <div className="flex rounded-lg overflow-hidden border border-slate-700 mb-6">
            <button
              id="tab-login"
              onClick={() => { setMode('login'); setError(''); }}
              className={`flex-1 py-2.5 text-sm font-semibold transition-all duration-200 ${
                mode === 'login'
                  ? 'bg-blue-600 text-white'
                  : 'text-slate-400 hover:text-white hover:bg-slate-800'
              }`}
            >
              Sign In
            </button>
            <button
              id="tab-register"
              onClick={() => { setMode('register'); setError(''); }}
              className={`flex-1 py-2.5 text-sm font-semibold transition-all duration-200 ${
                mode === 'register'
                  ? 'bg-blue-600 text-white'
                  : 'text-slate-400 hover:text-white hover:bg-slate-800'
              }`}
            >
              Create Account
            </button>
          </div>

          {/* Error banner */}
          {error && (
            <div className="mb-4 px-4 py-3 bg-red-500/10 border border-red-500/30 rounded-lg text-red-400 text-sm">
              ⚠ {error}
            </div>
          )}

          {/* LOGIN FORM */}
          {mode === 'login' && (
            <form onSubmit={handleLogin} className="space-y-4">
              <div>
                <label className="block text-xs font-mono text-slate-400 mb-1.5 tracking-widest uppercase">Email</label>
                <input
                  id="login-email"
                  type="email"
                  required
                  value={loginEmail}
                  onChange={e => setLoginEmail(e.target.value)}
                  placeholder="diplomat@france-unsc.org"
                  className="w-full bg-slate-800/60 border border-slate-600 rounded-lg px-4 py-3 text-white text-sm placeholder-slate-500 focus:outline-none focus:border-cyan-500 focus:ring-1 focus:ring-cyan-500/30 transition-all"
                />
              </div>
              <div>
                <label className="block text-xs font-mono text-slate-400 mb-1.5 tracking-widest uppercase">Password</label>
                <input
                  id="login-password"
                  type="password"
                  required
                  value={loginPassword}
                  onChange={e => setLoginPassword(e.target.value)}
                  placeholder="••••••••"
                  className="w-full bg-slate-800/60 border border-slate-600 rounded-lg px-4 py-3 text-white text-sm placeholder-slate-500 focus:outline-none focus:border-cyan-500 focus:ring-1 focus:ring-cyan-500/30 transition-all"
                />
              </div>
              <button
                id="login-submit"
                type="submit"
                disabled={loading}
                className="w-full py-3 bg-gradient-to-r from-blue-600 to-cyan-600 hover:from-blue-500 hover:to-cyan-500 text-white font-semibold rounded-lg transition-all duration-200 shadow-lg shadow-blue-500/20 disabled:opacity-50 disabled:cursor-not-allowed mt-2"
              >
                {loading ? 'Authenticating...' : '→ Access Command Center'}
              </button>

              {/* Demo credentials hint */}
              <div className="mt-3 px-3 py-2 bg-slate-800/50 rounded-lg border border-slate-700/50 text-xs text-slate-500 font-mono">
                <span className="text-slate-400">Admin demo:</span> admin@france-unsc.org / admin123
              </div>
            </form>
          )}

          {/* REGISTER FORM */}
          {mode === 'register' && (
            <form onSubmit={handleRegister} className="space-y-4">
              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className="block text-xs font-mono text-slate-400 mb-1.5 tracking-widest uppercase">Full Name</label>
                  <input
                    id="reg-fullname"
                    type="text"
                    required
                    value={regFullName}
                    onChange={e => setRegFullName(e.target.value)}
                    placeholder="Jean Dupont"
                    className="w-full bg-slate-800/60 border border-slate-600 rounded-lg px-3 py-2.5 text-white text-sm placeholder-slate-500 focus:outline-none focus:border-cyan-500 focus:ring-1 focus:ring-cyan-500/30 transition-all"
                  />
                </div>
                <div>
                  <label className="block text-xs font-mono text-slate-400 mb-1.5 tracking-widest uppercase">Username</label>
                  <input
                    id="reg-username"
                    type="text"
                    required
                    value={regUsername}
                    onChange={e => setRegUsername(e.target.value)}
                    placeholder="jdupont"
                    className="w-full bg-slate-800/60 border border-slate-600 rounded-lg px-3 py-2.5 text-white text-sm placeholder-slate-500 focus:outline-none focus:border-cyan-500 focus:ring-1 focus:ring-cyan-500/30 transition-all"
                  />
                </div>
              </div>
              <div>
                <label className="block text-xs font-mono text-slate-400 mb-1.5 tracking-widest uppercase">Email</label>
                <input
                  id="reg-email"
                  type="email"
                  required
                  value={regEmail}
                  onChange={e => setRegEmail(e.target.value)}
                  placeholder="diplomat@france-unsc.org"
                  className="w-full bg-slate-800/60 border border-slate-600 rounded-lg px-4 py-2.5 text-white text-sm placeholder-slate-500 focus:outline-none focus:border-cyan-500 focus:ring-1 focus:ring-cyan-500/30 transition-all"
                />
              </div>
              <div>
                <label className="block text-xs font-mono text-slate-400 mb-1.5 tracking-widest uppercase">Country Assignment</label>
                <select
                  id="reg-country"
                  value={regCountry}
                  onChange={e => setRegCountry(e.target.value)}
                  className="w-full bg-slate-800/60 border border-slate-600 rounded-lg px-4 py-2.5 text-white text-sm focus:outline-none focus:border-cyan-500 focus:ring-1 focus:ring-cyan-500/30 transition-all"
                >
                  {COUNTRIES.map(c => (
                    <option key={c} value={c}>{c}</option>
                  ))}
                </select>
              </div>
              <div>
                <label className="block text-xs font-mono text-slate-400 mb-1.5 tracking-widest uppercase">Password</label>
                <input
                  id="reg-password"
                  type="password"
                  required
                  minLength={6}
                  value={regPassword}
                  onChange={e => setRegPassword(e.target.value)}
                  placeholder="Min. 6 characters"
                  className="w-full bg-slate-800/60 border border-slate-600 rounded-lg px-4 py-2.5 text-white text-sm placeholder-slate-500 focus:outline-none focus:border-cyan-500 focus:ring-1 focus:ring-cyan-500/30 transition-all"
                />
              </div>
              <button
                id="register-submit"
                type="submit"
                disabled={loading}
                className="w-full py-3 bg-gradient-to-r from-blue-600 to-cyan-600 hover:from-blue-500 hover:to-cyan-500 text-white font-semibold rounded-lg transition-all duration-200 shadow-lg shadow-blue-500/20 disabled:opacity-50 disabled:cursor-not-allowed"
              >
                {loading ? 'Creating account...' : '→ Join Command Center'}
              </button>
            </form>
          )}
        </div>

        <p className="text-center text-xs text-slate-600 mt-4 font-mono">
          UN CHARTER ART. 24 & 27 · CLASSIFIED SYSTEM · AUTHORIZED PERSONNEL ONLY
        </p>
      </div>
    </div>
  );
}
