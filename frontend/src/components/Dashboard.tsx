import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { 
  Mic, 
  TrendingUp, 
  Calendar, 
  Award, 
  Play, 
  BarChart3, 
  User,
  LogOut,
  Plus,
  BookOpen,
  Users,
  Eye,
  Hand,
  Lightbulb,
  Target,
  Clock
} from 'lucide-react';
import { useAuth } from '../context/AuthContext';

const Dashboard = () => {
  const { user, logout } = useAuth();
  const navigate = useNavigate();
  const [activeTab, setActiveTab] = useState('overview');

  const handleLogout = () => {
    logout();
    navigate('/');
  };

  // Mock data for recent sessions
  const recentSessions = [
    {
      id: '1',
      type: 'Speech Practice',
      duration: '5 min',
      score: 85,
      date: '2024-01-15',
      improvement: '+5'
    },
    {
      id: '2',
      type: 'Interview Practice',
      duration: '10 min',
      score: 78,
      date: '2024-01-14',
      improvement: '+2'
    },
    {
      id: '3',
      type: 'Conversation',
      duration: '3 min',
      score: 82,
      date: '2024-01-13',
      improvement: '+8'
    }
  ];

  const stats = [
    { label: 'Overall Score', value: user?.overallScore || 0, icon: Award, color: 'text-blue-600' },
    { label: 'Total Sessions', value: user?.totalSessions || 0, icon: Play, color: 'text-green-600' },
    { label: 'This Month', value: 8, icon: Calendar, color: 'text-purple-600' },
    { label: 'Improvement', value: '+12%', icon: TrendingUp, color: 'text-orange-600' }
  ];

  const bodyLanguageTips = [
    {
      title: 'Power Posture',
      description: 'Stand tall with shoulders back and feet shoulder-width apart',
      icon: User,
      category: 'Posture'
    },
    {
      title: 'Open Gestures',
      description: 'Keep arms uncrossed and use open palm gestures to appear trustworthy',
      icon: Hand,
      category: 'Gestures'
    },
    {
      title: 'Eye Contact Rule',
      description: 'Maintain eye contact for 3-5 seconds, then shift naturally',
      icon: Eye,
      category: 'Eye Contact'
    },
    {
      title: 'Confident Stance',
      description: 'Avoid swaying or shifting weight - plant your feet firmly',
      icon: Target,
      category: 'Stability'
    }
  ];

  const speakingTips = [
    {
      title: 'The 3-Second Rule',
      description: 'Pause for 3 seconds before answering difficult questions',
      icon: Clock,
      category: 'Timing'
    },
    {
      title: 'Tell Stories',
      description: 'Use personal anecdotes to make your points more memorable',
      icon: BookOpen,
      category: 'Content'
    },
    {
      title: 'Mirror Your Audience',
      description: 'Match the energy and tone of your audience for better connection',
      icon: Users,
      category: 'Connection'
    },
    {
      title: 'Practice Out Loud',
      description: 'Always rehearse speeches aloud, not just in your head',
      icon: Mic,
      category: 'Practice'
    }
  ];

  const exercises = [
    {
      title: 'Mirror Practice',
      description: 'Practice your speech in front of a mirror for 10 minutes daily',
      duration: '10 min',
      difficulty: 'Easy'
    },
    {
      title: 'Record & Review',
      description: 'Record yourself speaking and analyze your body language',
      duration: '15 min',
      difficulty: 'Medium'
    },
    {
      title: 'Impromptu Speaking',
      description: 'Pick random topics and speak for 2 minutes without preparation',
      duration: '20 min',
      difficulty: 'Hard'
    },
    {
      title: 'Breathing Exercise',
      description: 'Practice diaphragmatic breathing to control nerves',
      duration: '5 min',
      difficulty: 'Easy'
    }
  ];

  const renderOverview = () => (
    <>
      {/* Stats Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
        {stats.map((stat, index) => (
          <div key={index} className="bg-white p-6 rounded-xl shadow-lg hover:shadow-xl transition-shadow">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-gray-600 mb-1">{stat.label}</p>
                <p className="text-2xl font-bold text-gray-900">{stat.value}</p>
              </div>
              <div className={`h-12 w-12 rounded-lg bg-gray-50 flex items-center justify-center ${stat.color}`}>
                <stat.icon className="h-6 w-6" />
              </div>
            </div>
          </div>
        ))}
      </div>

      <div className="grid lg:grid-cols-3 gap-8">
        {/* Quick Actions */}
        <div className="lg:col-span-2">
          <div className="bg-white rounded-xl shadow-lg p-6 mb-8">
            <h2 className="text-xl font-semibold text-gray-900 mb-6">Quick Start</h2>
            <div className="grid md:grid-cols-3 gap-4">
              <Link
                to="/record/speech"
                className="group p-6 border-2 border-gray-200 rounded-lg hover:border-blue-500 hover:bg-blue-50 transition-all duration-200"
              >
                <div className="h-12 w-12 bg-blue-100 rounded-lg flex items-center justify-center mb-4 group-hover:bg-blue-200 transition-colors">
                  <Mic className="h-6 w-6 text-blue-600" />
                </div>
                <h3 className="font-semibold text-gray-900 mb-2">Speech Practice</h3>
                <p className="text-sm text-gray-600">Practice public speaking with or without a script</p>
              </Link>

              <Link
                to="/record/interview"
                className="group p-6 border-2 border-gray-200 rounded-lg hover:border-purple-500 hover:bg-purple-50 transition-all duration-200"
              >
                <div className="h-12 w-12 bg-purple-100 rounded-lg flex items-center justify-center mb-4 group-hover:bg-purple-200 transition-colors">
                  <User className="h-6 w-6 text-purple-600" />
                </div>
                <h3 className="font-semibold text-gray-900 mb-2">Interview Practice</h3>
                <p className="text-sm text-gray-600">Practice with industry-specific questions</p>
              </Link>

              <Link
                to="/record/conversation"
                className="group p-6 border-2 border-gray-200 rounded-lg hover:border-green-500 hover:bg-green-50 transition-all duration-200"
              >
                <div className="h-12 w-12 bg-green-100 rounded-lg flex items-center justify-center mb-4 group-hover:bg-green-200 transition-colors">
                  <BarChart3 className="h-6 w-6 text-green-600" />
                </div>
                <h3 className="font-semibold text-gray-900 mb-2">Conversation</h3>
                <p className="text-sm text-gray-600">General analysis of natural conversation</p>
              </Link>
            </div>
          </div>

          {/* Recent Sessions */}
          <div className="bg-white rounded-xl shadow-lg p-6">
            <div className="flex justify-between items-center mb-6">
              <h2 className="text-xl font-semibold text-gray-900">Recent Sessions</h2>
              <Link 
                to="/record" 
                className="text-blue-600 hover:text-blue-700 font-medium flex items-center space-x-1"
              >
                <Plus className="h-4 w-4" />
                <span>New Session</span>
              </Link>
            </div>
            <div className="space-y-4">
              {recentSessions.map((session) => (
                <div key={session.id} className="flex items-center justify-between p-4 border border-gray-200 rounded-lg hover:bg-gray-50 transition-colors">
                  <div className="flex items-center space-x-4">
                    <div className="h-10 w-10 bg-blue-100 rounded-lg flex items-center justify-center">
                      <Play className="h-5 w-5 text-blue-600" />
                    </div>
                    <div>
                      <h3 className="font-medium text-gray-900">{session.type}</h3>
                      <p className="text-sm text-gray-600">{session.duration} • {session.date}</p>
                    </div>
                  </div>
                  <div className="flex items-center space-x-4">
                    <div className="text-right">
                      <p className="font-semibold text-gray-900">{session.score}/100</p>
                      <p className="text-sm text-green-600">+{session.improvement}</p>
                    </div>
                    <Link
                      to={`/results/${session.id}`}
                      className="text-blue-600 hover:text-blue-700 font-medium"
                    >
                      View
                    </Link>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>

        {/* Progress Chart */}
        <div className="bg-white rounded-xl shadow-lg p-6">
          <h2 className="text-xl font-semibold text-gray-900 mb-6">Progress Overview</h2>
          <div className="space-y-6">
            <div>
              <div className="flex justify-between text-sm mb-2">
                <span className="text-gray-600">Speech Clarity</span>
                <span className="font-medium">85%</span>
              </div>
              <div className="w-full bg-gray-200 rounded-full h-2">
                <div className="bg-blue-600 h-2 rounded-full" style={{ width: '85%' }}></div>
              </div>
            </div>
            
            <div>
              <div className="flex justify-between text-sm mb-2">
                <span className="text-gray-600">Body Language</span>
                <span className="font-medium">72%</span>
              </div>
              <div className="w-full bg-gray-200 rounded-full h-2">
                <div className="bg-purple-600 h-2 rounded-full" style={{ width: '72%' }}></div>
              </div>
            </div>
            
            <div>
              <div className="flex justify-between text-sm mb-2">
                <span className="text-gray-600">Confidence</span>
                <span className="font-medium">78%</span>
              </div>
              <div className="w-full bg-gray-200 rounded-full h-2">
                <div className="bg-green-600 h-2 rounded-full" style={{ width: '78%' }}></div>
              </div>
            </div>
            
            <div>
              <div className="flex justify-between text-sm mb-2">
                <span className="text-gray-600">Engagement</span>
                <span className="font-medium">81%</span>
              </div>
              <div className="w-full bg-gray-200 rounded-full h-2">
                <div className="bg-orange-600 h-2 rounded-full" style={{ width: '81%' }}></div>
              </div>
            </div>
          </div>

          <div className="mt-8 p-4 bg-gradient-to-r from-blue-50 to-purple-50 rounded-lg">
            <h3 className="font-semibold text-gray-900 mb-2">Next Goal</h3>
            <p className="text-sm text-gray-600 mb-3">
              Improve your body language score to reach 80%
            </p>
            <div className="w-full bg-gray-200 rounded-full h-2">
              <div className="bg-gradient-to-r from-blue-600 to-purple-600 h-2 rounded-full" style={{ width: '72%' }}></div>
            </div>
            <p className="text-xs text-gray-500 mt-1">8% to go</p>
          </div>
        </div>
      </div>
    </>
  );

  const renderBodyLanguageTips = () => (
    <div className="space-y-8">
      {/* Tips Grid */}
      <div className="bg-white rounded-xl shadow-lg p-8">
        <h2 className="text-2xl font-semibold text-gray-900 mb-6">Body Language Essentials</h2>
        <div className="grid md:grid-cols-2 gap-6">
          {bodyLanguageTips.map((tip, index) => (
            <div key={index} className="p-6 border border-gray-200 rounded-lg hover:shadow-md transition-shadow">
              <div className="flex items-start space-x-4">
                <div className="h-12 w-12 bg-blue-100 rounded-lg flex items-center justify-center flex-shrink-0">
                  <tip.icon className="h-6 w-6 text-blue-600" />
                </div>
                <div>
                  <div className="flex items-center space-x-2 mb-2">
                    <h3 className="font-semibold text-gray-900">{tip.title}</h3>
                    <span className="px-2 py-1 bg-gray-100 text-xs font-medium text-gray-600 rounded-full">
                      {tip.category}
                    </span>
                  </div>
                  <p className="text-gray-600 text-sm leading-relaxed">{tip.description}</p>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Quick Reference */}
      <div className="bg-white rounded-xl shadow-lg p-8">
        <h3 className="text-xl font-semibold text-gray-900 mb-6">Quick Reference Guide</h3>
        <div className="grid md:grid-cols-3 gap-6">
          <div className="text-center p-6 bg-green-50 rounded-lg">
            <div className="h-12 w-12 bg-green-100 rounded-lg flex items-center justify-center mx-auto mb-4">
              <Target className="h-6 w-6 text-green-600" />
            </div>
            <h4 className="font-semibold text-gray-900 mb-2">Do This</h4>
            <ul className="text-sm text-gray-600 space-y-1">
              <li>• Stand tall and straight</li>
              <li>• Use open gestures</li>
              <li>• Maintain eye contact</li>
              <li>• Smile naturally</li>
            </ul>
          </div>

          <div className="text-center p-6 bg-red-50 rounded-lg">
            <div className="h-12 w-12 bg-red-100 rounded-lg flex items-center justify-center mx-auto mb-4">
              <User className="h-6 w-6 text-red-600" />
            </div>
            <h4 className="font-semibold text-gray-900 mb-2">Avoid This</h4>
            <ul className="text-sm text-gray-600 space-y-1">
              <li>• Crossing arms</li>
              <li>• Looking down</li>
              <li>• Fidgeting</li>
              <li>• Slouching</li>
            </ul>
          </div>

          <div className="text-center p-6 bg-blue-50 rounded-lg">
            <div className="h-12 w-12 bg-blue-100 rounded-lg flex items-center justify-center mx-auto mb-4">
              <Lightbulb className="h-6 w-6 text-blue-600" />
            </div>
            <h4 className="font-semibold text-gray-900 mb-2">Pro Tips</h4>
            <ul className="text-sm text-gray-600 space-y-1">
              <li>• Practice in mirror</li>
              <li>• Record yourself</li>
              <li>• Get feedback</li>
              <li>• Stay consistent</li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  );

  const renderSpeakingTips = () => (
    <div className="space-y-8">
      {/* Speaking Tips */}
      <div className="bg-white rounded-xl shadow-lg p-8">
        <h2 className="text-2xl font-semibold text-gray-900 mb-6">Public Speaking Best Practices</h2>
        <div className="grid md:grid-cols-2 gap-6">
          {speakingTips.map((tip, index) => (
            <div key={index} className="p-6 border border-gray-200 rounded-lg hover:shadow-md transition-shadow">
              <div className="flex items-start space-x-4">
                <div className="h-12 w-12 bg-purple-100 rounded-lg flex items-center justify-center flex-shrink-0">
                  <tip.icon className="h-6 w-6 text-purple-600" />
                </div>
                <div>
                  <div className="flex items-center space-x-2 mb-2">
                    <h3 className="font-semibold text-gray-900">{tip.title}</h3>
                    <span className="px-2 py-1 bg-gray-100 text-xs font-medium text-gray-600 rounded-full">
                      {tip.category}
                    </span>
                  </div>
                  <p className="text-gray-600 text-sm leading-relaxed">{tip.description}</p>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Practice Exercises */}
      <div className="bg-white rounded-xl shadow-lg p-8">
        <h3 className="text-xl font-semibold text-gray-900 mb-6">Practice Exercises</h3>
        <div className="space-y-4">
          {exercises.map((exercise, index) => (
            <div key={index} className="p-6 border border-gray-200 rounded-lg hover:bg-gray-50 transition-colors">
              <div className="flex items-center justify-between">
                <div className="flex-1">
                  <div className="flex items-center space-x-3 mb-2">
                    <h4 className="font-semibold text-gray-900">{exercise.title}</h4>
                    <span className={`px-2 py-1 text-xs font-medium rounded-full ${
                      exercise.difficulty === 'Easy' ? 'bg-green-100 text-green-700' :
                      exercise.difficulty === 'Medium' ? 'bg-yellow-100 text-yellow-700' :
                      'bg-red-100 text-red-700'
                    }`}>
                      {exercise.difficulty}
                    </span>
                  </div>
                  <p className="text-gray-600 text-sm mb-2">{exercise.description}</p>
                  <div className="flex items-center text-sm text-gray-500">
                    <Clock className="h-4 w-4 mr-1" />
                    {exercise.duration}
                  </div>
                </div>
                <button className="ml-4 bg-blue-600 text-white px-4 py-2 rounded-lg text-sm font-medium hover:bg-blue-700 transition-colors">
                  Try Now
                </button>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Speaking Framework */}
      <div className="bg-white rounded-xl shadow-lg p-8">
        <h3 className="text-xl font-semibold text-gray-900 mb-6">The STAR Framework</h3>
        <div className="grid md:grid-cols-4 gap-6">
          <div className="text-center p-4 bg-blue-50 rounded-lg">
            <div className="h-10 w-10 bg-blue-100 rounded-lg flex items-center justify-center mx-auto mb-3">
              <span className="font-bold text-blue-600">S</span>
            </div>
            <h4 className="font-semibold text-gray-900 mb-2">Situation</h4>
            <p className="text-sm text-gray-600">Set the context</p>
          </div>
          <div className="text-center p-4 bg-purple-50 rounded-lg">
            <div className="h-10 w-10 bg-purple-100 rounded-lg flex items-center justify-center mx-auto mb-3">
              <span className="font-bold text-purple-600">T</span>
            </div>
            <h4 className="font-semibold text-gray-900 mb-2">Task</h4>
            <p className="text-sm text-gray-600">Explain the challenge</p>
          </div>
          <div className="text-center p-4 bg-green-50 rounded-lg">
            <div className="h-10 w-10 bg-green-100 rounded-lg flex items-center justify-center mx-auto mb-3">
              <span className="font-bold text-green-600">A</span>
            </div>
            <h4 className="font-semibold text-gray-900 mb-2">Action</h4>
            <p className="text-sm text-gray-600">Describe what you did</p>
          </div>
          <div className="text-center p-4 bg-orange-50 rounded-lg">
            <div className="h-10 w-10 bg-orange-100 rounded-lg flex items-center justify-center mx-auto mb-3">
              <span className="font-bold text-orange-600">R</span>
            </div>
            <h4 className="font-semibold text-gray-900 mb-2">Result</h4>
            <p className="text-sm text-gray-600">Share the outcome</p>
          </div>
        </div>
      </div>
    </div>
  );

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 to-blue-50">
      {/* Navigation */}
      <nav className="bg-white/80 backdrop-blur-md border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            <div className="flex items-center space-x-2">
              <Mic className="h-8 w-8 text-blue-600" />
              <span className="text-xl font-bold text-gray-900">PresenceAI</span>
            </div>
            <div className="flex items-center space-x-4">
              <div className="flex items-center space-x-2 text-gray-700">
                <User className="h-5 w-5" />
                <span className="font-medium">{user?.name}</span>
              </div>
              <button
                onClick={handleLogout}
                className="flex items-center space-x-1 text-gray-600 hover:text-red-600 transition-colors"
              >
                <LogOut className="h-5 w-5" />
                <span>Logout</span>
              </button>
            </div>
          </div>
        </div>
      </nav>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Welcome Section */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900 mb-2">
            Welcome back, {user?.name?.split(' ')[0]}!
          </h1>
          <p className="text-gray-600">
            Ready to continue improving your speaking skills?
          </p>
        </div>

        {/* Tab Navigation */}
        <div className="mb-8">
          <div className="border-b border-gray-200">
            <nav className="-mb-px flex space-x-8">
              <button
                onClick={() => setActiveTab('overview')}
                className={`py-2 px-1 border-b-2 font-medium text-sm ${
                  activeTab === 'overview'
                    ? 'border-blue-500 text-blue-600'
                    : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                }`}
              >
                Overview
              </button>
              <button
                onClick={() => setActiveTab('body-language')}
                className={`py-2 px-1 border-b-2 font-medium text-sm ${
                  activeTab === 'body-language'
                    ? 'border-blue-500 text-blue-600'
                    : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                }`}
              >
                Body Language Tips
              </button>
              <button
                onClick={() => setActiveTab('speaking-tips')}
                className={`py-2 px-1 border-b-2 font-medium text-sm ${
                  activeTab === 'speaking-tips'
                    ? 'border-blue-500 text-blue-600'
                    : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                }`}
              >
                Speaking Tips & Practices
              </button>
            </nav>
          </div>
        </div>

        {/* Tab Content */}
        {activeTab === 'overview' && renderOverview()}
        {activeTab === 'body-language' && renderBodyLanguageTips()}
        {activeTab === 'speaking-tips' && renderSpeakingTips()}
      </div>
    </div>
  );
};

export default Dashboard;