import React from 'react';
import { Link } from 'react-router-dom';
import { Mic, User, MessageCircle, Clock, Target, Users, ArrowLeft } from 'lucide-react';

const RecordingHub = () => {
  const recordingModes = [
    {
      id: 'speech',
      title: 'Speech Practice',
      description: 'Practice public speaking with timed sessions',
      icon: Mic,
      color: 'blue',
      features: ['1, 5, or 10 minute sessions', 'Script optional', 'Posture & gesture tracking'],
      path: '/record/speech'
    },
    {
      id: 'interview',
      title: 'Interview Practice',
      description: 'Industry-specific interview questions',
      icon: User,
      color: 'purple',
      features: ['Industry selection', 'Relevant questions', 'Professional assessment'],
      path: '/record/interview'
    },
    {
      id: 'conversation',
      title: 'Conversation Analysis',
      description: 'Natural conversation skills assessment',
      icon: MessageCircle,
      color: 'green',
      features: ['General analysis', 'Movement tracking', 'Speech patterns'],
      path: '/record/conversation'
    }
  ];

  const getColorClasses = (color: string) => {
    const colorMap = {
      blue: {
        bg: 'bg-blue-50',
        border: 'border-blue-200 hover:border-blue-400',
        icon: 'bg-blue-100 text-blue-600',
        button: 'bg-blue-600 hover:bg-blue-700'
      },
      purple: {
        bg: 'bg-purple-50',
        border: 'border-purple-200 hover:border-purple-400',
        icon: 'bg-purple-100 text-purple-600',
        button: 'bg-purple-600 hover:bg-purple-700'
      },
      green: {
        bg: 'bg-green-50',
        border: 'border-green-200 hover:border-green-400',
        icon: 'bg-green-100 text-green-600',
        button: 'bg-green-600 hover:bg-green-700'
      }
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
              <Mic className="h-8 w-8 text-blue-600" />
              <span className="text-xl font-bold text-gray-900">PresenceAI</span>
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

      <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        {/* Header */}
        <div className="text-center mb-12">
          <h1 className="text-4xl font-bold text-gray-900 mb-4">Choose Your Practice Mode</h1>
          <p className="text-xl text-gray-600 max-w-3xl mx-auto">
            Select the type of speaking practice that matches your goals. Each mode provides specialized feedback and analysis.
          </p>
        </div>

        {/* Recording Mode Cards */}
        <div className="grid md:grid-cols-1 lg:grid-cols-3 gap-8 mb-12">
          {recordingModes.map((mode) => {
            const colors = getColorClasses(mode.color);
            return (
              <div
                key={mode.id}
                className={`${colors.bg} border-2 ${colors.border} rounded-2xl p-8 transition-all duration-300 hover:shadow-xl`}
              >
                <div className={`h-16 w-16 ${colors.icon} rounded-xl flex items-center justify-center mb-6`}>
                  <mode.icon className="h-8 w-8" />
                </div>

                <h3 className="text-2xl font-bold text-gray-900 mb-3">{mode.title}</h3>
                <p className="text-gray-600 mb-6 leading-relaxed">{mode.description}</p>

                <ul className="space-y-3 mb-8">
                  {mode.features.map((feature, index) => (
                    <li key={index} className="flex items-center text-gray-700">
                      <div className="h-2 w-2 bg-gray-400 rounded-full mr-3"></div>
                      {feature}
                    </li>
                  ))}
                </ul>

                <Link
                  to={mode.path}
                  className={`w-full ${colors.button} text-white py-3 px-6 rounded-lg font-semibold transition-all duration-200 transform hover:scale-105 block text-center`}
                >
                  Start Practice
                </Link>
              </div>
            );
          })}
        </div>

        {/* Tips Section */}
        <div className="bg-white rounded-2xl shadow-lg p-8">
          <h2 className="text-2xl font-bold text-gray-900 mb-6 text-center">Practice Tips</h2>
          <div className="grid md:grid-cols-3 gap-8">
            <div className="text-center">
              <div className="h-12 w-12 bg-blue-100 rounded-lg flex items-center justify-center mx-auto mb-4">
                <Target className="h-6 w-6 text-blue-600" />
              </div>
              <h3 className="font-semibold text-gray-900 mb-2">Set Clear Goals</h3>
              <p className="text-gray-600">Focus on specific areas you want to improve each session</p>
            </div>

            <div className="text-center">
              <div className="h-12 w-12 bg-purple-100 rounded-lg flex items-center justify-center mx-auto mb-4">
                <Clock className="h-6 w-6 text-purple-600" />
              </div>
              <h3 className="font-semibold text-gray-900 mb-2">Practice Regularly</h3>
              <p className="text-gray-600">Consistent short sessions are more effective than long infrequent ones</p>
            </div>

            <div className="text-center">
              <div className="h-12 w-12 bg-green-100 rounded-lg flex items-center justify-center mx-auto mb-4">
                <Users className="h-6 w-6 text-green-600" />
              </div>
              <h3 className="font-semibold text-gray-900 mb-2">Review Feedback</h3>
              <p className="text-gray-600">Study your results to understand improvement areas</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default RecordingHub;