import React from 'react';
import { Link, useParams } from 'react-router-dom';
import { 
  ArrowLeft, 
  TrendingUp, 
  TrendingDown, 
  Award, 
  Clock,
  Eye,
  Mic,
  User,
  MessageCircle,
  BarChart3,
  Target,
  Play
} from 'lucide-react';

const ResultsPage = () => {
  const { sessionId } = useParams();
  
  // Mock data based on session type
  const getSessionData = () => {
    if (sessionId?.startsWith('speech')) {
      return {
        type: 'Speech Practice',
        icon: Mic,
        color: 'blue',
        duration: '5:00',
        overallScore: 85,
        improvement: '+5',
        date: new Date().toLocaleDateString()
      };
    } else if (sessionId?.startsWith('interview')) {
      return {
        type: 'Interview Practice',
        icon: User,
        color: 'purple',
        duration: '12:30',
        overallScore: 78,
        improvement: '+2',
        date: new Date().toLocaleDateString()
      };
    } else {
      return {
        type: 'Conversation Analysis',
        icon: MessageCircle,
        color: 'green',
        duration: '8:45',
        overallScore: 82,
        improvement: '+8',
        date: new Date().toLocaleDateString()
      };
    }
  };

  const sessionData = getSessionData();

  const metrics = [
    {
      category: 'Speech Clarity',
      score: 88,
      change: '+3',
      description: 'Clear pronunciation and articulation',
      suggestions: ['Slow down during complex points', 'Practice tongue twisters']
    },
    {
      category: 'Body Language',
      score: 72,
      change: '+8',
      description: 'Posture, gestures, and movement',
      suggestions: ['Keep shoulders back', 'Use deliberate hand gestures']
    },
    {
      category: 'Eye Contact',
      score: 85,
      change: '+2',
      description: 'Natural and engaging eye contact',
      suggestions: ['Excellent progress!', 'Continue current approach']
    },
    {
      category: 'Confidence',
      score: 79,
      change: '+5',
      description: 'Overall presence and self-assurance',
      suggestions: ['Practice power poses', 'Embrace natural pauses']
    }
  ];

  const getScoreColor = (score: number) => {
    if (score >= 80) return 'text-green-600 bg-green-50';
    if (score >= 60) return 'text-yellow-600 bg-yellow-50';
    return 'text-red-600 bg-red-50';
  };

  const getColorClasses = (color: string) => {
    const colorMap = {
      blue: 'bg-blue-100 text-blue-600',
      purple: 'bg-purple-100 text-purple-600',
      green: 'bg-green-100 text-green-600'
    };
    return colorMap[color as keyof typeof colorMap];
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 to-blue-50">
      {/* Navigation */}
      <nav className="bg-white/80 backdrop-blur-md border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            <div className="flex items-center space-x-2">
              <sessionData.icon className="h-8 w-8 text-gray-700" />
              <span className="text-xl font-bold text-gray-900">Session Results</span>
            </div>
            <Link
              to="/dashboard"
              className="flex items-center space-x-2 text-gray-600 hover:text-gray-900 transition-colors"
            >
              <ArrowLeft className="h-4 w-4" />
              <span>Back to Dashboard</span>
            </Link>
          </div>
        </div>
      </nav>

      <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Session Overview */}
        <div className="bg-white rounded-2xl shadow-lg p-8 mb-8">
          <div className="flex items-center justify-between mb-6">
            <div className="flex items-center space-x-4">
              <div className={`h-16 w-16 rounded-xl flex items-center justify-center ${getColorClasses(sessionData.color)}`}>
                <sessionData.icon className="h-8 w-8" />
              </div>
              <div>
                <h1 className="text-3xl font-bold text-gray-900">{sessionData.type}</h1>
                <p className="text-gray-600">{sessionData.date} • {sessionData.duration}</p>
              </div>
            </div>
            <div className="text-right">
              <div className="text-4xl font-bold text-gray-900 mb-1">{sessionData.overallScore}/100</div>
              <div className="flex items-center text-green-600">
                <TrendingUp className="h-4 w-4 mr-1" />
                <span className="font-medium">{sessionData.improvement}</span>
              </div>
            </div>
          </div>

          <div className="grid md:grid-cols-4 gap-6">
            <div className="text-center p-4 bg-gray-50 rounded-lg">
              <Award className="h-8 w-8 text-yellow-500 mx-auto mb-2" />
              <div className="font-semibold text-gray-900">Overall Grade</div>
              <div className="text-sm text-gray-600">Excellent</div>
            </div>
            <div className="text-center p-4 bg-gray-50 rounded-lg">
              <Clock className="h-8 w-8 text-blue-500 mx-auto mb-2" />
              <div className="font-semibold text-gray-900">Duration</div>
              <div className="text-sm text-gray-600">{sessionData.duration}</div>
            </div>
            <div className="text-center p-4 bg-gray-50 rounded-lg">
              <BarChart3 className="h-8 w-8 text-purple-500 mx-auto mb-2" />
              <div className="font-semibold text-gray-900">Progress</div>
              <div className="text-sm text-gray-600">+12% this month</div>
            </div>
            <div className="text-center p-4 bg-gray-50 rounded-lg">
              <Target className="h-8 w-8 text-green-500 mx-auto mb-2" />
              <div className="font-semibold text-gray-900">Goal Status</div>
              <div className="text-sm text-gray-600">On track</div>
            </div>
          </div>
        </div>

        <div className="grid lg:grid-cols-3 gap-8">
          {/* Detailed Metrics */}
          <div className="lg:col-span-2">
            <div className="bg-white rounded-2xl shadow-lg p-8">
              <h2 className="text-2xl font-bold text-gray-900 mb-6">Performance Breakdown</h2>
              <div className="space-y-6">
                {metrics.map((metric, index) => (
                  <div key={index} className="border-b border-gray-200 pb-6 last:border-b-0">
                    <div className="flex justify-between items-start mb-3">
                      <div>
                        <h3 className="font-semibold text-gray-900">{metric.category}</h3>
                        <p className="text-sm text-gray-600">{metric.description}</p>
                      </div>
                      <div className="text-right">
                        <div className={`inline-flex items-center px-3 py-1 rounded-full text-sm font-medium ${getScoreColor(metric.score)}`}>
                          {metric.score}/100
                        </div>
                        <div className="flex items-center text-green-600 text-sm mt-1">
                          <TrendingUp className="h-3 w-3 mr-1" />
                          {metric.change}
                        </div>
                      </div>
                    </div>
                    
                    <div className="mb-3">
                      <div className="w-full bg-gray-200 rounded-full h-2">
                        <div 
                          className="bg-gradient-to-r from-blue-600 to-purple-600 h-2 rounded-full transition-all duration-500"
                          style={{ width: `${metric.score}%` }}
                        ></div>
                      </div>
                    </div>

                    <div>
                      <h4 className="text-sm font-medium text-gray-900 mb-2">Key Actions:</h4>
                      <ul className="space-y-1">
                        {metric.suggestions.map((suggestion, idx) => (
                          <li key={idx} className="text-sm text-gray-600 flex items-start">
                            <span className="h-1.5 w-1.5 bg-gray-400 rounded-full mt-2 mr-2 flex-shrink-0"></span>
                            {suggestion}
                          </li>
                        ))}
                      </ul>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>

          {/* Insights & Actions */}
          <div className="space-y-8">
            {/* Key Insights */}
            <div className="bg-white rounded-2xl shadow-lg p-6">
              <h3 className="text-lg font-semibold text-gray-900 mb-4">Key Insights</h3>
              <div className="space-y-4">
                <div className="p-4 bg-green-50 rounded-lg">
                  <div className="flex items-start space-x-3">
                    <TrendingUp className="h-5 w-5 text-green-600 mt-0.5" />
                    <div>
                      <h4 className="font-medium text-green-900">Strong Improvement</h4>
                      <p className="text-sm text-green-700">Body language improved significantly</p>
                    </div>
                  </div>
                </div>

                <div className="p-4 bg-blue-50 rounded-lg">
                  <div className="flex items-start space-x-3">
                    <Eye className="h-5 w-5 text-blue-600 mt-0.5" />
                    <div>
                      <h4 className="font-medium text-blue-900">Eye Contact</h4>
                      <p className="text-sm text-blue-700">Excellent natural eye contact maintained</p>
                    </div>
                  </div>
                </div>

                <div className="p-4 bg-yellow-50 rounded-lg">
                  <div className="flex items-start space-x-3">
                    <Target className="h-5 w-5 text-yellow-600 mt-0.5" />
                    <div>
                      <h4 className="font-medium text-yellow-900">Focus Area</h4>
                      <p className="text-sm text-yellow-700">Work on posture consistency</p>
                    </div>
                  </div>
                </div>
              </div>
            </div>

            {/* Next Steps */}
            <div className="bg-white rounded-2xl shadow-lg p-6">
              <h3 className="text-lg font-semibold text-gray-900 mb-4">Recommended Next Steps</h3>
              <div className="space-y-3">
                <Link
                  to="/record/speech"
                  className="w-full bg-blue-600 text-white py-3 px-4 rounded-lg font-medium hover:bg-blue-700 transition-colors flex items-center justify-center space-x-2"
                >
                  <Play className="h-4 w-4" />
                  <span>Practice Again</span>
                </Link>
                
                <Link
                  to="/record"
                  className="w-full border border-gray-300 text-gray-700 py-3 px-4 rounded-lg font-medium hover:bg-gray-50 transition-colors text-center block"
                >
                  Try Different Mode
                </Link>
                
                <button className="w-full bg-gray-100 text-gray-700 py-3 px-4 rounded-lg font-medium hover:bg-gray-200 transition-colors">
                  Share Results
                </button>
              </div>
            </div>

            {/* Progress Goal */}
            <div className="bg-gradient-to-r from-blue-50 to-purple-50 rounded-2xl p-6">
              <h3 className="text-lg font-semibold text-gray-900 mb-4">Progress Goal</h3>
              <div className="text-center">
                <div className="text-3xl font-bold text-gray-900 mb-2">85/100</div>
                <p className="text-sm text-gray-600 mb-4">Target Score</p>
                <div className="w-full bg-gray-200 rounded-full h-3 mb-2">
                  <div 
                    className="bg-gradient-to-r from-blue-600 to-purple-600 h-3 rounded-full"
                    style={{ width: '85%' }}
                  ></div>
                </div>
                <p className="text-xs text-gray-500">You're almost there! Keep practicing.</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ResultsPage;