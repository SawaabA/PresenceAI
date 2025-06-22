import React, { useState, useRef, useEffect } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { 
  ArrowLeft, 
  Play, 
  Pause, 
  Square, 
  Mic, 
  Clock, 
  FileText,
  Video,
  CheckCircle
} from 'lucide-react';

const SpeechRecording = () => {
  const [selectedDuration, setSelectedDuration] = useState(5);
  const [hasScript, setHasScript] = useState(false);
  const [script, setScript] = useState('');
  const [isRecording, setIsRecording] = useState(false);
  const [isPaused, setIsPaused] = useState(false);
  const [timeRemaining, setTimeRemaining] = useState(0);
  const [recordingStep, setRecordingStep] = useState('setup'); // setup, recording, completed
  
  const videoRef = useRef<HTMLVideoElement>(null);
  const intervalRef = useRef<NodeJS.Timeout>();
  const navigate = useNavigate();

  const durations = [1, 5, 10];

  useEffect(() => {
    if (recordingStep === 'recording' && !isPaused) {
      setTimeRemaining(selectedDuration * 60);
      startCamera();
    }
    
    return () => {
      if (intervalRef.current) {
        clearInterval(intervalRef.current);
      }
    };
  }, [recordingStep, selectedDuration]);

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
    
    intervalRef.current = setInterval(() => {
      setTimeRemaining((prev) => {
        if (prev <= 1) {
          stopRecording();
          return 0;
        }
        return prev - 1;
      });
    }, 1000);
  };

  const pauseRecording = () => {
    setIsPaused(!isPaused);
    if (intervalRef.current) {
      if (isPaused) {
        intervalRef.current = setInterval(() => {
          setTimeRemaining((prev) => {
            if (prev <= 1) {
              stopRecording();
              return 0;
            }
            return prev - 1;
          });
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
    // Generate mock session ID and navigate to results
    const sessionId = 'speech-' + Date.now();
    navigate(`/results/${sessionId}`);
  };

  if (recordingStep === 'completed') {
    return (
      <div className="min-h-screen bg-gradient-to-br from-slate-50 to-blue-50 flex items-center justify-center">
        <div className="bg-white rounded-2xl shadow-xl p-8 max-w-md w-full mx-4 text-center">
          <div className="h-16 w-16 bg-green-100 rounded-full flex items-center justify-center mx-auto mb-6">
            <CheckCircle className="h-8 w-8 text-green-600" />
          </div>
          <h2 className="text-2xl font-bold text-gray-900 mb-4">Recording Complete!</h2>
          <p className="text-gray-600 mb-8">
            Your speech has been recorded and is being analyzed. You'll see your results in a moment.
          </p>
          <div className="space-y-3">
            <button
              onClick={handleComplete}
              className="w-full bg-blue-600 text-white py-3 rounded-lg font-semibold hover:bg-blue-700 transition-colors"
            >
              View Results
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
              <span className="text-white font-medium">Recording</span>
            </div>
            <div className="flex items-center space-x-2 text-white">
              <Clock className="h-4 w-4" />
              <span className="text-lg font-mono">{formatTime(timeRemaining)}</span>
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
            
            {hasScript && (
              <div className="absolute bottom-4 left-4 right-4 bg-black/70 text-white p-4 rounded-lg max-h-32 overflow-y-auto">
                <p className="text-sm leading-relaxed">{script}</p>
              </div>
            )}
          </div>
        </div>

        {/* Recording Status */}
        <div className="bg-black/50 p-4 text-center">
          <p className="text-white text-sm">
            {isPaused ? 'Recording paused' : 'Speak naturally and maintain good posture'}
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
              <Mic className="h-8 w-8 text-blue-600" />
              <span className="text-xl font-bold text-gray-900">PresenceAI</span>
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
          <h1 className="text-4xl font-bold text-gray-900 mb-4">Speech Practice Setup</h1>
          <p className="text-xl text-gray-600">
            Configure your speaking session and start practicing
          </p>
        </div>

        <div className="bg-white rounded-2xl shadow-xl p-8">
          {/* Duration Selection */}
          <div className="mb-8">
            <h3 className="text-lg font-semibold text-gray-900 mb-4 flex items-center">
              <Clock className="h-5 w-5 mr-2 text-blue-600" />
              Duration
            </h3>
            <div className="grid grid-cols-3 gap-4">
              {durations.map((duration) => (
                <button
                  key={duration}
                  onClick={() => setSelectedDuration(duration)}
                  className={`p-4 rounded-lg border-2 transition-all ${
                    selectedDuration === duration
                      ? 'border-blue-500 bg-blue-50 text-blue-700'
                      : 'border-gray-200 hover:border-gray-300'
                  }`}
                >
                  <div className="text-2xl font-bold">{duration}</div>
                  <div className="text-sm text-gray-600">minute{duration > 1 ? 's' : ''}</div>
                </button>
              ))}
            </div>
          </div>

          {/* Script Option */}
          <div className="mb-8">
            <h3 className="text-lg font-semibold text-gray-900 mb-4 flex items-center">
              <FileText className="h-5 w-5 mr-2 text-blue-600" />
              Script (Optional)
            </h3>
            <div className="flex items-center space-x-4 mb-4">
              <label className="flex items-center">
                <input
                  type="radio"
                  name="script"
                  checked={!hasScript}
                  onChange={() => setHasScript(false)}
                  className="h-4 w-4 text-blue-600"
                />
                <span className="ml-2">No script</span>
              </label>
              <label className="flex items-center">
                <input
                  type="radio"
                  name="script"
                  checked={hasScript}
                  onChange={() => setHasScript(true)}
                  className="h-4 w-4 text-blue-600"
                />
                <span className="ml-2">Use script</span>
              </label>
            </div>
            
            {hasScript && (
              <textarea
                value={script}
                onChange={(e) => setScript(e.target.value)}
                placeholder="Enter your speech script here..."
                className="w-full h-32 p-4 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent resize-none"
              />
            )}
          </div>

          {/* Camera Preview */}
          <div className="mb-8">
            <h3 className="text-lg font-semibold text-gray-900 mb-4 flex items-center">
              <Video className="h-5 w-5 mr-2 text-blue-600" />
              Camera Check
            </h3>
            <div className="bg-gray-100 rounded-lg p-8 text-center">
              <Video className="h-16 w-16 text-gray-400 mx-auto mb-4" />
              <p className="text-gray-600 mb-4">Camera will activate when you start recording</p>
              <p className="text-sm text-gray-500">
                Make sure you have good lighting and are positioned in frame
              </p>
            </div>
          </div>

          {/* Start Button */}
          <div className="text-center">
            <button
              onClick={startRecording}
              className="bg-gradient-to-r from-blue-600 to-purple-600 text-white px-12 py-4 rounded-lg font-semibold text-lg hover:opacity-90 transition-all duration-200 transform hover:scale-105 flex items-center space-x-2 mx-auto"
            >
              <Play className="h-6 w-6" />
              <span>Start Recording</span>
            </button>
            <p className="text-sm text-gray-500 mt-4">
              Recording will start immediately. Make sure you're ready to speak.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default SpeechRecording;