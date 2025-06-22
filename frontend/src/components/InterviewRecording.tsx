import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { ArrowLeft, User, Play, CheckCircle, Briefcase } from 'lucide-react';

const InterviewRecording = () => {
  const [selectedIndustry, setSelectedIndustry] = useState('');
  const [currentQuestion, setCurrentQuestion] = useState(0);
  const [isRecording, setIsRecording] = useState(false);
  const [recordingStep, setRecordingStep] = useState('setup'); // setup, interview, completed
  
  const navigate = useNavigate();

  const industries = [
    {
      id: 'technology',
      name: 'Technology',
      icon: '💻',
      questions: [
        'Tell me about a challenging technical project you worked on.',
        'How do you stay updated with the latest technology trends?',
        'Describe a time when you had to learn a new technology quickly.',
        'How would you explain a complex technical concept to a non-technical person?'
      ]
    },
    {
      id: 'finance',
      name: 'Finance',
      icon: '💰',
      questions: [
        'How do you analyze financial risks in your decision-making?',
        'Describe your experience with financial modeling.',
        'Tell me about a time you identified a cost-saving opportunity.',
        'How do you stay informed about market trends?'
      ]
    },
    {
      id: 'healthcare',
      name: 'Healthcare',
      icon: '🏥',
      questions: [
        'How do you handle high-pressure situations in healthcare?',
        'Describe your approach to patient communication.',
        'Tell me about a time you improved a healthcare process.',
        'How do you stay current with medical best practices?'
      ]
    },
    {
      id: 'marketing',
      name: 'Marketing',
      icon: '📈',
      questions: [
        'How do you measure the success of a marketing campaign?',
        'Describe a creative marketing solution you developed.',
        'Tell me about a time you had to pivot a marketing strategy.',
        'How do you identify target audiences for new products?'
      ]
    },
    {
      id: 'education',
      name: 'Education',
      icon: '🎓',
      questions: [
        'How do you adapt your teaching style for different learners?',
        'Describe a time you helped a struggling student succeed.',
        'Tell me about an innovative teaching method you used.',
        'How do you handle classroom management challenges?'
      ]
    },
    {
      id: 'sales',
      name: 'Sales',
      icon: '💼',
      questions: [
        'How do you build rapport with potential clients?',
        'Describe your approach to handling objections.',
        'Tell me about your most challenging sale.',
        'How do you maintain long-term client relationships?'
      ]
    }
  ];

  const selectedIndustryData = industries.find(ind => ind.id === selectedIndustry);

  const startInterview = () => {
    if (!selectedIndustry) return;
    setRecordingStep('interview');
    setCurrentQuestion(0);
    setIsRecording(true);
  };

  const nextQuestion = () => {
    if (selectedIndustryData && currentQuestion < selectedIndustryData.questions.length - 1) {
      setCurrentQuestion(currentQuestion + 1);
    } else {
      completeInterview();
    }
  };

  const completeInterview = () => {
    setIsRecording(false);
    setRecordingStep('completed');
  };

  const handleComplete = () => {
    const sessionId = 'interview-' + Date.now();
    navigate(`/results/${sessionId}`);
  };

  if (recordingStep === 'completed') {
    return (
      <div className="min-h-screen bg-gradient-to-br from-slate-50 to-blue-50 flex items-center justify-center">
        <div className="bg-white rounded-2xl shadow-xl p-8 max-w-md w-full mx-4 text-center">
          <div className="h-16 w-16 bg-green-100 rounded-full flex items-center justify-center mx-auto mb-6">
            <CheckCircle className="h-8 w-8 text-green-600" />
          </div>
          <h2 className="text-2xl font-bold text-gray-900 mb-4">Interview Complete!</h2>
          <p className="text-gray-600 mb-8">
            Great job! Your interview responses have been recorded and analyzed. View your performance report.
          </p>
          <div className="space-y-3">
            <button
              onClick={handleComplete}
              className="w-full bg-purple-600 text-white py-3 rounded-lg font-semibold hover:bg-purple-700 transition-colors"
            >
              View Results
            </button>
            <Link
              to="/record"
              className="w-full border border-gray-300 text-gray-700 py-3 rounded-lg font-semibold hover:bg-gray-50 transition-colors block"
            >
              Practice Again
            </Link>
          </div>
        </div>
      </div>
    );
  }

  if (recordingStep === 'interview') {
    return (
      <div className="min-h-screen bg-gradient-to-br from-purple-900 to-blue-900 text-white">
        {/* Interview Header */}
        <div className="bg-black/30 p-6 border-b border-white/20">
          <div className="max-w-4xl mx-auto flex justify-between items-center">
            <div className="flex items-center space-x-4">
              <div className="flex items-center space-x-2">
                <div className="h-3 w-3 bg-red-500 rounded-full animate-pulse"></div>
                <span className="font-medium">Recording Interview</span>
              </div>
              <div className="text-purple-200">
                Question {currentQuestion + 1} of {selectedIndustryData?.questions.length}
              </div>
            </div>
            <div className="text-purple-200">
              {selectedIndustryData?.name} Interview
            </div>
          </div>
        </div>

        {/* Question Display */}
        <div className="flex-1 flex items-center justify-center p-8">
          <div className="max-w-4xl w-full text-center">
            <div className="bg-white/10 backdrop-blur-md rounded-2xl p-12 mb-8">
              <h2 className="text-3xl font-bold mb-6">Interview Question</h2>
              <p className="text-xl leading-relaxed text-purple-100">
                {selectedIndustryData?.questions[currentQuestion]}
              </p>
            </div>
            
            <div className="flex justify-center space-x-4">
              <button
                onClick={nextQuestion}
                className="bg-purple-600 hover:bg-purple-700 text-white px-8 py-3 rounded-lg font-semibold transition-colors"
              >
                {currentQuestion < (selectedIndustryData?.questions.length || 0) - 1 ? 'Next Question' : 'Complete Interview'}
              </button>
              <button
                onClick={completeInterview}
                className="bg-white/20 hover:bg-white/30 text-white px-8 py-3 rounded-lg font-semibold transition-colors"
              >
                End Early
              </button>
            </div>
          </div>
        </div>

        {/* Instructions */}
        <div className="bg-black/30 p-4 text-center">
          <p className="text-purple-200 text-sm">
            Take your time to answer thoughtfully. Click "Next Question" when ready to continue.
          </p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 to-blue-50">
      {/* Navigation */}
      <nav className="bg-white/80 backdrop-blur-md border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            <div className="flex items-center space-x-2">
              <User className="h-8 w-8 text-purple-600" />
              <span className="text-xl font-bold text-gray-900">Interview Practice</span>
            </div>
            <Link
              to="/record"
              className="flex items-center space-x-2 text-gray-600 hover:text-gray-900 transition-colors"
            >
              <ArrowLeft className="h-4 w-4" />
              <span>Back</span>
            </Link>
          </div>
        </div>
      </nav>

      <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        {/* Header */}
        <div className="text-center mb-12">
          <h1 className="text-4xl font-bold text-gray-900 mb-4">Interview Practice Setup</h1>
          <p className="text-xl text-gray-600">
            Select your industry to practice with relevant interview questions
          </p>
        </div>

        <div className="bg-white rounded-2xl shadow-xl p-8">
          <h3 className="text-lg font-semibold text-gray-900 mb-6 flex items-center">
            <Briefcase className="h-5 w-5 mr-2 text-purple-600" />
            Choose Your Industry
          </h3>

          {/* Industry Selection */}
          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6 mb-8">
            {industries.map((industry) => (
              <button
                key={industry.id}
                onClick={() => setSelectedIndustry(industry.id)}
                className={`p-6 rounded-xl border-2 transition-all text-left ${
                  selectedIndustry === industry.id
                    ? 'border-purple-500 bg-purple-50'
                    : 'border-gray-200 hover:border-purple-300 hover:bg-purple-25'
                }`}
              >
                <div className="text-3xl mb-3">{industry.icon}</div>
                <h4 className="font-semibold text-gray-900 mb-2">{industry.name}</h4>
                <p className="text-sm text-gray-600">
                  {industry.questions.length} industry-specific questions
                </p>
              </button>
            ))}
          </div>

          {/* Selected Industry Preview */}
          {selectedIndustryData && (
            <div className="bg-purple-50 rounded-xl p-6 mb-8">
              <h4 className="font-semibold text-gray-900 mb-4">
                Preview: {selectedIndustryData.name} Questions
              </h4>
              <div className="space-y-2">
                {selectedIndustryData.questions.slice(0, 2).map((question, index) => (
                  <div key={index} className="flex items-start space-x-3">
                    <div className="h-6 w-6 bg-purple-200 rounded-full flex items-center justify-center text-sm font-medium text-purple-700">
                      {index + 1}
                    </div>
                    <p className="text-gray-700 text-sm">{question}</p>
                  </div>
                ))}
                <p className="text-sm text-purple-600 mt-3">
                  + {selectedIndustryData.questions.length - 2} more questions
                </p>
              </div>
            </div>
          )}

          {/* Interview Format Info */}
          <div className="bg-gray-50 rounded-xl p-6 mb-8">
            <h4 className="font-semibold text-gray-900 mb-4">How It Works</h4>
            <div className="grid md:grid-cols-3 gap-6">
              <div className="text-center">
                <div className="h-12 w-12 bg-purple-100 rounded-lg flex items-center justify-center mx-auto mb-3">
                  <span className="text-purple-600 font-bold">1</span>
                </div>
                <h5 className="font-medium text-gray-900 mb-2">Question Display</h5>
                <p className="text-sm text-gray-600">Each question appears on screen for you to read and prepare</p>
              </div>
              <div className="text-center">
                <div className="h-12 w-12 bg-purple-100 rounded-lg flex items-center justify-center mx-auto mb-3">
                  <span className="text-purple-600 font-bold">2</span>
                </div>
                <h5 className="font-medium text-gray-900 mb-2">Your Response</h5>
                <p className="text-sm text-gray-600">Answer naturally while being recorded for analysis</p>
              </div>
              <div className="text-center">
                <div className="h-12 w-12 bg-purple-100 rounded-lg flex items-center justify-center mx-auto mb-3">
                  <span className="text-purple-600 font-bold">3</span>
                </div>
                <h5 className="font-medium text-gray-900 mb-2">Progress</h5>
                <p className="text-sm text-gray-600">Continue through all questions at your own pace</p>
              </div>
            </div>
          </div>

          {/* Start Button */}
          <div className="text-center">
            <button
              onClick={startInterview}
              disabled={!selectedIndustry}
              className="bg-gradient-to-r from-purple-600 to-blue-600 text-white px-12 py-4 rounded-lg font-semibold text-lg hover:opacity-90 transition-all duration-200 transform hover:scale-105 flex items-center space-x-2 mx-auto disabled:opacity-50 disabled:transform-none"
            >
              <Play className="h-6 w-6" />
              <span>Start Interview</span>
            </button>
            <p className="text-sm text-gray-500 mt-4">
              {selectedIndustry ? 'Ready to begin your interview practice' : 'Please select an industry first'}
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default InterviewRecording;