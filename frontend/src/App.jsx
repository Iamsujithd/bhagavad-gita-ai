import React, { useState, useEffect, useRef } from 'react';
import axios from 'axios';
import { Send, Sun, BookOpen, Sparkles, Mic, Volume2, VolumeX } from 'lucide-react';

// Use relative /api path for Vercel production, local path for dev
const API_BASE = import.meta.env.PROD ? '/api' : 'http://127.0.0.1:8000/api';

export default function App() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const [dailyWisdom, setDailyWisdom] = useState(null);
  const [language, setLanguage] = useState('English');
  const [isSpeaking, setIsSpeaking] = useState(true);
  const [isListening, setIsListening] = useState(false);
  
  const messagesEndRef = useRef(null);
  
  // Speech Recognition Setup
  const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
  const recognition = SpeechRecognition ? new SpeechRecognition() : null;
  if (recognition) {
    recognition.continuous = false;
    recognition.lang = language === 'Kannada' ? 'kn-IN' : 'en-US';
  }

  useEffect(() => {
    // Fetch daily wisdom on load
    axios.get(`${API_BASE}/daily`).then(res => {
      setDailyWisdom(res.data);
    }).catch(err => console.error("Error fetching daily wisdom", err));
  }, []);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const toggleListen = () => {
    if (!recognition) return alert("Speech Recognition is not supported in this browser.");
    
    if (isListening) {
      recognition.stop();
      setIsListening(false);
    } else {
      recognition.start();
      setIsListening(true);
      recognition.onresult = (event) => {
        const transcript = event.results[0][0].transcript;
        setInput(prev => prev + " " + transcript);
        setIsListening(false);
      };
      recognition.onerror = () => setIsListening(false);
      recognition.onend = () => setIsListening(false);
    }
  };

  const speakText = (text) => {
    if (!isSpeaking || !window.speechSynthesis) return;
    
    // Stop any ongoing speech
    window.speechSynthesis.cancel();
    
    const utterance = new SpeechSynthesisUtterance(text);
    utterance.lang = language === 'Kannada' ? 'kn-IN' : 'en-US';
    // Optionally slow down the rate for better comprehension
    utterance.rate = 0.95; 
    window.speechSynthesis.speak(utterance);
  };

  const handleSend = async (e) => {
    e.preventDefault();
    if (!input.trim()) return;

    const userMessage = { role: 'user', content: input };
    const currentMessages = [...messages]; // capture history before adding new
    
    setMessages(prev => [...prev, userMessage]);
    setInput('');
    setLoading(true);

    try {
      const payload = { 
        query: userMessage.content, 
        language: language,
        history: currentMessages
      };
      const res = await axios.post(`${API_BASE}/chat`, payload);
      
      const aiMessage = { 
        role: 'ai', 
        content: res.data.answer,
        shlokas: res.data.shlokas 
      };
      
      setMessages(prev => [...prev, aiMessage]);
      
      // Read response aloud
      speakText(res.data.answer);
      
    } catch (error) {
      console.error(error);
      setMessages(prev => [...prev, { role: 'ai', content: "I'm sorry, I couldn't connect to the inner wisdom at this moment." }]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex flex-col items-center p-4 md:p-8 relative overflow-hidden bg-[#030712] text-slate-200">
      {/* Animated Ambient Orbs */}
      <div className="absolute top-0 left-1/4 w-96 h-96 bg-amber-600/10 rounded-full blur-[120px] animate-float -z-10 mix-blend-screen"></div>
      <div className="absolute bottom-1/4 right-1/4 w-[500px] h-[500px] bg-indigo-900/20 rounded-full blur-[150px] animate-float-delayed -z-10 mix-blend-screen"></div>
      <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-full h-full bg-[radial-gradient(ellipse_at_center,_var(--tw-gradient-stops))] from-amber-900/5 via-transparent to-transparent -z-20"></div>

      <header className="w-full max-w-5xl flex justify-between items-center mb-10 z-10 relative">
        <div className="flex items-center gap-4">
          <div className="relative">
            <div className="absolute inset-0 bg-amber-500 blur-md opacity-30 rounded-full"></div>
            <Sun className="w-10 h-10 text-amber-400 relative z-10 animate-[spin_60s_linear_infinite]" />
          </div>
          <div>
            <h1 className="text-3xl font-bold tracking-widest font-serif bg-clip-text text-transparent bg-gradient-to-r from-amber-200 to-amber-500">
              Gita AI
            </h1>
            <p className="text-xs tracking-[0.3em] text-slate-400 uppercase mt-1">Timeless Wisdom</p>
          </div>
        </div>
        
        <div className="flex items-center gap-4">
          <button 
            onClick={() => {
                setIsSpeaking(!isSpeaking);
                if (isSpeaking) window.speechSynthesis?.cancel();
            }}
            className="p-2 text-slate-400 hover:text-amber-400 transition-colors"
            title={isSpeaking ? "Mute AI Voice" : "Enable AI Voice"}
          >
            {isSpeaking ? <Volume2 className="w-5 h-5" /> : <VolumeX className="w-5 h-5" />}
          </button>

          <div className="glass-panel rounded-full px-1 py-1 flex items-center">
            <select 
              value={language}
              onChange={(e) => setLanguage(e.target.value)}
              className="bg-transparent text-slate-300 text-sm font-medium rounded-full px-4 py-2 outline-none focus:ring-1 focus:ring-amber-500/50 transition-all cursor-pointer appearance-none"
            >
              <option value="English" className="bg-slate-900 text-slate-200">English</option>
              <option value="Kannada" className="bg-slate-900 text-slate-200">ಕನ್ನಡ</option>
            </select>
          </div>
        </div>
      </header>

      <main className="w-full max-w-5xl grid grid-cols-1 lg:grid-cols-12 gap-8 flex-1 z-10 relative h-[75vh]">
        
        {/* Left Col: Daily Wisdom */}
        <div className="lg:col-span-4 flex flex-col h-full">
          {dailyWisdom && (
            <div className="glass-panel p-8 rounded-3xl h-full flex flex-col relative overflow-hidden group hover:border-amber-500/20 transition-all duration-500">
              <div className="absolute top-0 right-0 w-32 h-32 bg-amber-500/5 rounded-bl-[100px] -z-10 transition-all group-hover:bg-amber-500/10"></div>
              
              <div className="flex items-center gap-3 mb-8 text-amber-400">
                <Sparkles className="w-5 h-5" />
                <h2 className="font-serif tracking-widest uppercase text-sm font-bold">Daily Verse</h2>
              </div>
              
              <div className="flex-1 flex flex-col justify-center">
                <p className="text-xs font-bold uppercase tracking-widest text-slate-500 mb-4 border-b border-white/5 pb-2">
                  Chapter {dailyWisdom.chapter}, Verse {dailyWisdom.verse}
                </p>
                <p className="font-serif text-xl leading-relaxed text-amber-200/90 mb-6 whitespace-pre-line drop-shadow-md">
                  {dailyWisdom.sanskrit}
                </p>
                <p className="text-sm text-slate-300 leading-relaxed italic border-l-2 border-amber-500/30 pl-4 py-1">
                  "{dailyWisdom.translation}"
                </p>
              </div>
              
              <div className="mt-8 pt-6 border-t border-white/5">
                <p className="text-xs uppercase tracking-wider text-slate-500 mb-2">Theme</p>
                <div className="inline-block px-4 py-1.5 rounded-full bg-amber-500/10 text-amber-300 text-xs font-medium border border-amber-500/20">
                  {dailyWisdom.theme}
                </div>
              </div>
            </div>
          )}
        </div>

        {/* Right Col: Chat Interface */}
        <div className="lg:col-span-8 flex flex-col glass-panel rounded-3xl h-full overflow-hidden">
          
          <div className="flex-1 overflow-y-auto p-6 md:p-8 flex flex-col gap-6 scroll-smooth">
            {messages.length === 0 && (
              <div className="flex-1 flex flex-col items-center justify-center text-center">
                <div className="w-20 h-20 rounded-full bg-amber-500/5 flex items-center justify-center mb-6 border border-amber-500/10">
                  <BookOpen className="w-8 h-8 text-amber-400/50" />
                </div>
                <h3 className="font-serif text-xl text-slate-300 mb-2">Seek Inner Clarity</h3>
                <p className="text-slate-500 max-w-sm text-sm leading-relaxed">
                  Ask about duty, anxiety, relationships, or your path in life. The ancient wisdom will guide you.
                </p>
              </div>
            )}
            
            {messages.map((msg, i) => (
              <div key={i} className={`flex flex-col w-full message-enter ${msg.role === 'user' ? 'items-end' : 'items-start'}`}>
                
                {msg.role === 'ai' && msg.shlokas && msg.shlokas.length > 0 && (
                  <div className="mb-4 max-w-[85%] bg-slate-900/60 backdrop-blur-md border border-amber-500/20 rounded-2xl p-5 shadow-lg">
                    <div className="flex items-center gap-2 mb-3">
                      <div className="w-1.5 h-1.5 rounded-full bg-amber-500"></div>
                      <p className="text-[10px] font-bold uppercase tracking-widest text-amber-500/80">
                        Reference • Ch {msg.shlokas[0].chapter}, V {msg.shlokas[0].verse}
                      </p>
                    </div>
                    <p className="font-serif text-amber-100/90 mb-3 whitespace-pre-line leading-relaxed text-sm md:text-base">
                      {msg.shlokas[0].sanskrit}
                    </p>
                    <p className="text-sm text-slate-400 italic">"{msg.shlokas[0].translation}"</p>
                  </div>
                )}
                
                <div className={`px-6 py-4 max-w-[85%] rounded-2xl text-sm md:text-base leading-relaxed shadow-xl ${
                  msg.role === 'user' 
                    ? 'bg-amber-600/20 border border-amber-500/30 text-amber-50 rounded-tr-sm' 
                    : 'bg-slate-800/60 border border-white/5 text-slate-300 rounded-tl-sm whitespace-pre-line'
                }`}>
                  {msg.content}
                </div>
              </div>
            ))}
            
            {loading && (
              <div className="flex gap-2 p-6 text-amber-500/50 items-center bg-slate-800/30 rounded-2xl rounded-tl-sm w-max border border-white/5">
                <div className="w-2 h-2 rounded-full bg-current animate-bounce"></div>
                <div className="w-2 h-2 rounded-full bg-current animate-bounce" style={{animationDelay: '0.2s'}}></div>
                <div className="w-2 h-2 rounded-full bg-current animate-bounce" style={{animationDelay: '0.4s'}}></div>
              </div>
            )}
            <div ref={messagesEndRef} />
          </div>
          
          {/* Input Area */}
          <div className="p-4 md:p-6 bg-slate-900/50 border-t border-white/5 backdrop-blur-xl">
            <form onSubmit={handleSend} className="relative flex items-center w-full gap-2">
              <button 
                type="button"
                onClick={toggleListen}
                className={`flex items-center justify-center w-12 h-12 rounded-full transition-all border ${
                  isListening 
                    ? 'bg-red-500/20 border-red-500/50 text-red-400 animate-pulse' 
                    : 'bg-slate-800/50 border-white/10 text-slate-400 hover:text-amber-400 hover:border-amber-500/30'
                }`}
                title="Speak to Gita AI"
              >
                <Mic className="w-5 h-5" />
              </button>
              <div className="relative flex-1">
                <input 
                  type="text" 
                  value={input}
                  onChange={e => setInput(e.target.value)}
                  placeholder="Ask your question..." 
                  className="w-full glass-input rounded-full py-4 pl-6 pr-16 text-slate-200 placeholder:text-slate-500"
                />
                <button 
                  type="submit" 
                  disabled={loading || !input.trim()}
                  className="absolute right-2 top-1/2 -translate-y-1/2 flex items-center justify-center w-10 h-10 bg-amber-600 hover:bg-amber-500 text-white rounded-full transition-all disabled:opacity-50 disabled:hover:bg-amber-600 shadow-[0_0_15px_rgba(217,119,6,0.4)]"
                >
                  <Send className="w-4 h-4 ml-0.5" />
                </button>
              </div>
            </form>
          </div>
          
        </div>
      </main>
    </div>
  );
}
