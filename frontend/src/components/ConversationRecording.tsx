import React, { useState, useRef, useEffect } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { 
  ArrowLeft, 
  MessageCircle, 
  Play, 
  Pause, 
  Square, 
  CheckCircle,
  Video,
  Mic
} from 'lucide-react';

const ConversationRecording = () => {
  const [isRecording, setIsRecording] = useState(false);
  const [isPaused, setIsPaused] = useState(false);
  const [recordingTime, setRecordingTime] = useState(0);
  const [recordingStep, setRecordingStep] = useState('setup'); // setup, recording, completed
  
  const videoRef = useRef<HTMLVideoElement>(null);
  const intervalRef = useRef<NodeJS.Timeout>();
  const navigate = useNavigate();

  useEffect(() => {
    if (recordingStep === 'recording' && !isPaused) {
      startCamera();
    }
    
    return () => {
      if (intervalRef.current) {
        clearInterval(intervalRef.current);
      }
    };
  }, [recordingStep]);

  const startCamera = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ 
        video: true, 
        audio: true 
      });
      if (videoRef.current) {
        videoRef.current.srcObject = stream;
      }
    } catch (error) {
      console.error('Error accessing camera:', error);
    }
  };

  const startRecording = () => {
    setIsRecording(true);
    setRecordingStep('recording');
    setRecordingTime(0);
    
    intervalRef.current = setInterval(() => {
      setRecordingTime((prev) => prev + 1);
    }, 1000);
  };

  const pauseRecording = () => {
    setIsPaused(!isPaused);
    if (intervalRef.current) {
      if (isPaused) {
        intervalRef.current = setInterval(() => {
          setRecordingTime((prev) => prev + 1);
        }, 1000);
      } else {
        clearInterval(intervalRef.current);
      }
    }
  };

  const stopRecording = () => {
    setIsRecording(false);
    setIsPaused(false);
    if (intervalRef.current) {
      clearInterval(intervalRef.current);
    }
    setRecordingStep('completed');
    
    // Stop camera stream
    if (videoRef.current?.srcObject) {
      const stream = videoRef.current.srcObject as MediaStream;
      stream.getTracks().forEach(track => track.stop());
    }
  };

  const formatTime = (seconds: number) => {
    const mins = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${mins}:${secs.toString().padStart(2, '0')}`;
  };

  const handleComplete = () => {
    const sessionId = 'conversation-' + Date.now();
    navigate(`/results/${sessionId}`);
  };

  if (recordingStep === 'completed') {
    return (
      <div className="min-h-screen bg-gradient-to-br from-slate-50 to-blue-50 flex items-center justify-center">
        <div className="bg-white rounded-2xl shadow-xl p-8 max-w-md w-full mx-4 text-center">
          <div className="h-16 w-16 bg-green-100 rounded-full flex items-center justify-center mx-auto mb-6">
            <CheckCircle className="h-8 w-8 text-green-600" />
          </div>
          <h2 className="text-2xl font-bold text-gray-900 mb-4">Conversation Analyzed!</h2>
          <p className="text-gray-600 mb-8">
            Your conversation has been recorded and analyzed. Review your natural speaking patterns and body language.
          </p>
          <div className="space-y-3">
            <button
              onClick={handleComplete}
              className="w-full bg-green-600 text-white py-3 rounded-lg font-semibold hover:bg-green-700 transition-colors"
            >
              View Analysis
            </button>
            <Link
              to="/record"
              className="w-full border border-gray-300 text-gray-700 py-3 rounded-lg font-semibold hover:bg-gray-50 transition-colors block"
            >
              Record Another
            </Link>
          </div>
        </div>
      </div>
    );
  }

  if (recordingStep === 'recording') {
    return (
      <div className="min-h-screen bg-gray-900 flex flex-col">
        {/* Recording Header */}
        <div className="bg-black/50 p-4 flex justify-between items-center">
          <div className="flex items-center space-x-4">
            <div className="flex items-center space-x-2">
              <div className="h-3 w-3 bg-red-500 rounded-full animate-pulse"></div>
              <span className="text-white font-medium">Recording Conversation</span>
            </div>
            <div className="flex items-center space-x-2 text-white">
              <MessageCircle className="h-4 w-4" />
              <span className="text-lg font-mono">{formatTime(recordingTime)}</span>
            </div>
          </div>
          
          <div className="flex items-center space-x-3">
            <button
              onClick={pauseRecording}
              className="bg-yellow-600 hover:bg-yellow-700 text-white p-3 rounded-full transition-colors"
            >
              {isPaused ? <Play className="h-5 w-5" /> : <Pause className="h-5 w-5" />}
            </button>
            <button
              onClick={stopRecording}
              className="bg-red-600 hover:bg-red-700 text-white p-3 rounded-full transition-colors"
            >
              <Square className="h-5 w-5 fill-current" />
            </button>
          </div>
        </div>

        {/* Video Feed */}
        <div className="flex-1 flex items-center justify-center p-8">
          <div className="relative max-w-4xl w-full">
            <video
              ref={videoRef}
              autoPlay
              muted
              className="w-full h-auto rounded-lg shadow-xl"
              style={{ transform: 'scaleX(-1)' }}
            />
            
            {/* Conversation Topics Overlay */}
            <div className="absolute top-4 left-4 right-4 bg-black/70 text-white p-4 rounded-lg">
              <h3 className="font-semibold mb-2">Conversation Topics</h3>
              <div className="grid grid-cols-2 gap-2 text-sm">
                <span className="bg-green-600/20 px-2 py-1 rounded">• Current events</span>
                <span className="bg-blue-600/20 px-2 py-1 rounded">• Personal interests</span>
                <span className="bg-purple-600/20 px-2 py-1 rounded">• Travel experiences</span>
                <span className="bg-orange-600/20 px-2 py-1 rounded">• Future goals</span>
              </div>
            </div>
          </div>
        </div>

        {/* Recording Status */}
        <div className="bg-black/50 p-4 text-center">
          <p className="text-white text-sm">
            {isPaused ? 'Recording paused' : 'Speak naturally as if having a casual conversation'}
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
              <MessageCircle className="h-8 w-8 text-green-600" />
              <span className="text-xl font-bold text-gray-900">Conversation Analysis</span>
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

      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        {/* Header */}
        <div className="text-center mb-12">
          <h1 className="text-4xl font-bold text-gray-900 mb-4">Conversation Analysis</h1>
          <p className="text-xl text-gray-600">
            Practice natural conversation skills with comprehensive analysis
          </p>
        </div>

        <div className="bg-white rounded-2xl shadow-xl p-8">
          {/* What We Analyze */}
          <div className="mb-8">
            <h3 className="text-lg font-semibold text-gray-900 mb-6">What We'll Analyze</h3>
            <div className="grid md:grid-cols-3 gap-6">
              <div className="text-center p-6 bg-green-50 rounded-xl">
                <div className="h-12 w-12 bg-green-100 rounded-lg flex items-center justify-center mx-auto mb-4">
                  <Mic className="h-6 w-6 text-green-600" />
                </div>
                <h4 className="font-semibold text-gray-900 mb-2">Speech Patterns</h4>
                <p className="text-sm text-gray-600">Pace, tone, volume, and clarity of speech</p>
              </div>

              <div className="text-center p-6 bg-blue-50 rounded-xl">
                <div className="h-12 w-12 bg-blue-100 rounded-lg flex items-center justify-center mx-auto mb-4">
                  <Video className="h-6 w-6 text-blue-600" />
                </div>
                <h4 className="font-semibold text-gray-900 mb-2">Body Language</h4>
                <p className="text-sm text-gray-600">Posture, gestures, and facial expressions</p>
              </div>

              <div className="text-center p-6 bg-purple-50 rounded-xl">
                <div className="h-12 w-12 bg-purple-100 rounded-lg flex items-center justify-center mx-auto mb-4">
                  <MessageCircle className="h-6 w-6 text-purple-600" />
                </div>
                <h4 className="font-semibold text-gray-900 mb-2">Natural Flow</h4>
                <p className="text-sm text-gray-600">Conversational rhythm and engagement</p>
              </div>
            </div>
          </div>

          {/* Instructions */}
          <div className="mb-8">
            <h3 className="text-lg font-semibold text-gray-900 mb-4">Instructions</h3>
            <div className="bg-gray-50 rounded-xl p-6">
              <div className="space-y-4">
                <div className="flex items-start space-x-3">
                  <div className="h-6 w-6 bg-green-200 rounded-full flex items-center justify-center text-sm font-medium text-green-700 mt-0.5">
                    1
                  </div>
                  <div>
                    <h4 className="font-medium text-gray-900">Speak Naturally</h4>
                    <p className="text-sm text-gray-600">Talk as if you're having a casual conversation with a friend</p>
                  </div>
                </div>
                
                <div className="flex items-start space-x-3">
                  <div className="h-6 w-6 bg-green-200 rounded-full flex items-center justify-center text-sm font-medium text-green-700 mt-0.5">
                    2
                  </div>
                  <div>
                    <h4 className="font-medium text-gray-900">Cover Various Topics</h4>
                    <p className="text-sm text-gray-600">Discuss current events, interests, experiences, or any topic that comes to mind</p>
                  </div>
                </div>
                
                <div className="flex items-start space-x-3">
                  <div className="h-6 w-6 bg-green-200 rounded-full flex items-center justify-center text-sm font-medium text-green-700 mt-0.5">
                    3
                  </div>
                  <div>
                    <h4 className="font-medium text-gray-900">No Time Limit</h4>
                    <p className="text-sm text-gray-600">Record for as long as you'd like - stop when you feel you've captured enough</p>
                  </div>
                </div>
              </div>
            </div>
          </div>

          {/* Camera Preview */}
          <div className="mb-8">
            <h3 className="text-lg font-semibold text-gray-900 mb-4 flex items-center">
              <Video className="h-5 w-5 mr-2 text-green-600" />
              Camera Setup
            </h3>
            <div className="bg-gray-100 rounded-lg p-8 text-center">
              <Video className="h-16 w-16 text-gray-400 mx-auto mb-4" />
              <p className="text-gray-600 mb-4">Camera will activate when you start recording</p>
              <p className="text-sm text-gray-500">
                Position yourself comfortably - this should feel like a natural conversation
              </p>
            </div>
          </div>

          {/* Start Button */}
          <div className="text-center">
            <button
              onClick={startRecording}
              className="bg-gradient-to-r from-green-600 to-blue-600 text-white px-12 py-4 rounded-lg font-semibold text-lg hover:opacity-90 transition-all duration-200 transform hover:scale-105 flex items-center space-x-2 mx-auto"
            >
              <Play className="h-6 w-6" />
              <span>Start Conversation</span>
            </button>
            <p className="text-sm text-gray-500 mt-4">
              Begin speaking naturally about any topic you'd like
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ConversationRecording;