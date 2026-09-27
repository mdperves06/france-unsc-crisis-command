import React, { useState, useEffect } from 'react';
import { TopCommandBar } from './components/TopCommandBar';
import { ModeWorldIntelligence } from './components/ModeWorldIntelligence';
import { ModeCrisisTrainer } from './components/ModeCrisisTrainer';
import { ModePracticeArena } from './components/ModePracticeArena';
import { FranceCommandCenter } from './components/FranceCommandCenter';
import { UNSCDatabase } from './components/UNSCDatabase';
import { LabsView } from './components/LabsView';
import { AnalyticsView } from './components/AnalyticsView';
import { AuthPage } from './components/AuthPage';
import { getStoredUser, authLogout, authStatus } from './lib/api';

export function App() {
  const [currentTab, setCurrentTab] = useState<string>('world');
  const [unscYear, setUnscYear] = useState<number>(2026);
  const [activeRegion, setActiveRegion] = useState<string>('Middle East');
  const [activeScenarioId, setActiveScenarioId] = useState<string>('scenario-default');
  const [currentUser, setCurrentUser] = useState<any | null>(null);
  const [authChecked, setAuthChecked] = useState(false);

  // On mount: check if user is already logged in via stored token
  useEffect(() => {
    const storedUser = getStoredUser();
    if (storedUser) {
      // Verify token is still valid
      authStatus()
        .then(status => {
          if (status.authenticated) {
            setCurrentUser(status.user);
          } else {
            authLogout(); // Clear stale token
          }
        })
        .catch(() => {
          // Backend not reachable — use stored user for offline graceful degradation
          setCurrentUser(storedUser);
        })
        .finally(() => setAuthChecked(true));
    } else {
      setAuthChecked(true);
    }
  }, []);

  function handleAuthenticated(user: any) {
    setCurrentUser(user);
  }

  function handleLogout() {
    authLogout();
    setCurrentUser(null);
    setCurrentTab('world');
  }

  const handleLaunchTraining = (regionName: string) => {
    setActiveRegion(regionName);
    setCurrentTab('trainer');
  };

  const handleLaunchPractice = (regionName: string) => {
    setActiveRegion(regionName);
    setCurrentTab('arena');
  };

  const handleAdvanceToPractice = (scenarioId: string) => {
    setActiveScenarioId(scenarioId);
    setCurrentTab('arena');
  };

  // Show nothing while we're checking auth (avoid flash)
  if (!authChecked) {
    return (
      <div className="min-h-screen bg-[#050814] flex items-center justify-center">
        <div className="text-cyan-400 font-mono text-sm animate-pulse tracking-widest">
          INITIALIZING COMMAND SYSTEMS...
        </div>
      </div>
    );
  }

  // Show login/register if not authenticated
  if (!currentUser) {
    return <AuthPage onAuthenticated={handleAuthenticated} />;
  }

  return (
    <div className="min-h-screen bg-[#050814] text-slate-100 tactical-grid flex flex-col selection:bg-cyan-500 selection:text-black">
      {/* Top Command Bar */}
      <TopCommandBar
        currentTab={currentTab}
        onTabChange={setCurrentTab}
        unscYear={unscYear}
        onYearChange={setUnscYear}
        alertsCount={3}
        currentUser={currentUser}
        onLogout={handleLogout}
      />

      {/* Main Workspace Body */}
      <main className="flex-1 pb-12">
        {currentTab === 'world' && (
          <ModeWorldIntelligence
            onLaunchTraining={handleLaunchTraining}
            onLaunchPractice={handleLaunchPractice}
          />
        )}

        {currentTab === 'trainer' && (
          <ModeCrisisTrainer
            initialRegion={activeRegion}
            onAdvanceToPractice={handleAdvanceToPractice}
          />
        )}

        {currentTab === 'arena' && (
          <ModePracticeArena scenarioId={activeScenarioId} />
        )}

        {currentTab === 'france' && <FranceCommandCenter />}

        {currentTab === 'unsc' && <UNSCDatabase unscYear={unscYear} />}

        {currentTab === 'labs' && <LabsView />}

        {currentTab === 'analytics' && <AnalyticsView />}
      </main>

      {/* Persistent Mission Command Footer */}
      <footer className="bg-slate-950/90 border-t border-slate-900 py-3 px-4 text-center text-xs font-mono text-slate-500 flex flex-col sm:flex-row items-center justify-between max-w-[1720px] mx-auto w-full">
        <div>
          FRANCE UNSC CRISIS COMMAND // PERMANENT MISSION OF FRANCE TO THE UNITED NATIONS
        </div>
        <div className="flex items-center space-x-3 text-[11px] text-slate-400">
          {currentUser && (
            <span className="text-cyan-400">
              {currentUser.full_name.toUpperCase()} · {currentUser.country_assignment}
            </span>
          )}
          <span>&bull;</span>
          <span>AI RUNTIME: HYBRID (4 SPECIALIST AGENTS)</span>
          <span>&bull;</span>
          <span className="text-cyan-400">UN CHARTER ARTICLE 24 &amp; 27 COMPLIANT</span>
        </div>
      </footer>
    </div>
  );
}

export default App;
