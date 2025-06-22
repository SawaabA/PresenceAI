import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import LandingPage from './components/LandingPage';
import AuthPage from './components/AuthPage';
import Dashboard from './components/Dashboard';
import RecordingHub from './components/RecordingHub';
import SpeechRecording from './components/SpeechRecording';
import InterviewRecording from './components/InterviewRecording';
import ConversationRecording from './components/ConversationRecording';
import ResultsPage from './components/ResultsPage';
import { AuthProvider } from './context/AuthContext';

function App() {
  return (
    <AuthProvider>
      <Router>
        <div className="min-h-screen bg-gradient-to-br from-slate-50 to-blue-50">
          <Routes>
            <Route path="/" element={<LandingPage />} />
            <Route path="/auth" element={<AuthPage />} />
            <Route path="/dashboard" element={<Dashboard />} />
            <Route path="/record" element={<RecordingHub />} />
            <Route path="/record/speech" element={<SpeechRecording />} />
            <Route path="/record/interview" element={<InterviewRecording />} />
            <Route path="/record/conversation" element={<ConversationRecording />} />
            <Route path="/results/:sessionId" element={<ResultsPage />} />
          </Routes>
        </div>
      </Router>
    </AuthProvider>
  );
}

export default App;