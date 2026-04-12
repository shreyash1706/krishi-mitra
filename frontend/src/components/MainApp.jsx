import { useState, useEffect, useRef } from 'react';
import axios from 'axios';
import { 
  LogOut, PlusCircle, MessageSquare, Menu, X, Send, 
  MapPin, User, ChevronDown, ChevronUp, Bot, BrainCircuit, Tractor, Trash2
} from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';
import clsx from 'clsx';

// Helper to render basic markdown bold (**) safely
const renderFormattedText = (text, isThinking = false) => {
  if (!text) return null;
  const parts = text.split(/(\*\*.*?\*\*)/g);
  return (
    <div className={clsx("whitespace-pre-wrap", isThinking ? "font-normal" : "font-medium")}>
      {parts.map((p, i) => {
        if (p.startsWith('**') && p.endsWith('**') && p.length > 4) {
          return <strong key={i} className={isThinking ? "font-bold text-slate-800" : "font-extrabold text-slate-900"}>{p.slice(2, -2)}</strong>;
        }
        return <span key={i}>{p}</span>;
      })}
    </div>
  );
};

export default function MainApp({ user, onLogout }) {
  const [sessions, setSessions] = useState([]);
  const [activeSessionId, setActiveSessionId] = useState(null);
  const [messages, setMessages] = useState([]);
  const [language, setLanguage] = useState("English");
  
  const [input, setInput] = useState("");
  const [isSidebarOpen, setIsSidebarOpen] = useState(true);
  const [isGenerating, setIsGenerating] = useState(false);
  
  const messagesEndRef = useRef(null);

  useEffect(() => {
    const fetchSessions = async () => {
      try {
        const res = await axios.get(`http://127.0.0.1:8000/sessions/${user.user_id}`);
        setSessions(res.data.sessions || []);
      } catch (err) {
        console.error("Failed to load sessions", err);
      }
    };
    fetchSessions();
  }, [user.user_id]);

  const loadHistory = async (sessionId) => {
    try {
      const res = await axios.get(`http://127.0.0.1:8000/history/${sessionId}`);
      const formatted = res.data.messages.map(m => ({
        role: m.role,
        content: m.content,
        agent: m.role === 'assistant' ? "System" : undefined,
      }));
      setMessages(formatted);
      setActiveSessionId(sessionId);
      if (window.innerWidth < 768) setIsSidebarOpen(false);
    } catch (err) {
      console.error("Failed to load history", err);
    }
  };

  const deleteChat = async (sessionId, e) => {
    e.stopPropagation();
    try {
      await axios.delete(`http://127.0.0.1:8000/sessions/${sessionId}`);
      setSessions(prev => prev.filter(s => s.session_id !== sessionId));
      if (activeSessionId === sessionId) {
        createNewChat();
      }
    } catch (err) {
      console.error("Failed to delete chat", err);
    }
  };

  const createNewChat = () => {
    setActiveSessionId(null);
    setMessages([
      { role: "assistant", content: `Namaskar ${user.name}! How can I help you today?`, agent: "system" }
    ]);
    if (window.innerWidth < 768) setIsSidebarOpen(false);
  };

  useEffect(() => {
    if (!activeSessionId && messages.length === 0) {
      createNewChat();
    }
  }, []);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };
  useEffect(scrollToBottom, [messages]);

  const handleSubmit = async (e) => {
    if (e) e.preventDefault();
    if (!input.trim() || isGenerating) return;

    const userMsg = input.trim();
    setInput("");
    
    setMessages(prev => [...prev, { role: "user", content: userMsg }]);
    
    setMessages(prev => [
      ...prev, 
      { role: "assistant", content: "", reasoning: "", agent: "Thinking...", isStreaming: true }
    ]);
    
    setIsGenerating(true);

    try {
      const payload = {
        user_id: user.user_id,
        query: userMsg,
        output_language: language,
        ...(activeSessionId && { session_id: activeSessionId })
      };

      const response = await fetch("http://127.0.0.1:8000/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload)
      });

      if (!response.ok) throw new Error("Network error");

      const reader = response.body.getReader();
      const decoder = new TextDecoder("utf-8");
      
      let tempContent = "";
      let tempReasoning = "";
      let tempAgent = "Thinking...";
      let buffer = "";

      while (true) {
        const { value, done } = await reader.read();
        if (done) break;
        
        buffer += decoder.decode(value, { stream: true });
        const lines = buffer.split('\n');
        
        // The last element is either an empty string (if buffer ended with \n) 
        // or a partial line. We keep it in the buffer for the next chunk.
        buffer = lines.pop() || "";
        
        for (const line of lines) {
          if (!line.trim()) continue;
          try {
            const data = JSON.parse(line);
            if (data.agent) tempAgent = data.agent;
            if (!activeSessionId && data.session_id) setActiveSessionId(data.session_id);
            
            if (data.reasoning) tempReasoning += data.reasoning;
            if (data.chunk) tempContent += data.chunk;
            
            setMessages(prev => {
              const newMsgs = [...prev];
              newMsgs[newMsgs.length - 1] = {
                role: "assistant",
                content: tempContent,
                reasoning: tempReasoning,
                agent: tempAgent,
                isStreaming: true
              };
              return newMsgs;
            });
            
          } catch (e) {
            console.error("JSON parse error on line:", line, e);
          }
        }
      }
      
      setMessages(prev => {
        const newMsgs = [...prev];
        const lastMsg = newMsgs[newMsgs.length - 1];
        lastMsg.isStreaming = false;
        
        // Final cleanup for dangling tool_calls if any
        let cleanText = lastMsg.content?.replace(/<tool_call>.*?<\/tool_call>/gs, '') || "";
        if (cleanText.includes("<tool_call>")) cleanText = cleanText.substring(0, cleanText.lastIndexOf("<tool_call>"));
        lastMsg.content = cleanText;
        
        return newMsgs;
      });
      
    } catch (err) {
      console.error(err);
      setMessages(prev => {
        const newMsgs = [...prev];
        newMsgs[newMsgs.length - 1] = { 
          role: "assistant", 
          content: "Sorry, I had trouble connecting to the Krishi Mitra servers.", 
          agent: "system" 
        };
        return newMsgs;
      });
    } finally {
      setIsGenerating(false);
      const res = await axios.get(`http://127.0.0.1:8000/sessions/${user.user_id}`);
      setSessions(res.data.sessions || []);
    }
  };

  return (
    <div className="flex h-screen overflow-hidden text-slate-900 bg-slate-50 font-sans">
      
      {/* SIDEBAR */}
      <div className={clsx(
        "fixed inset-y-0 left-0 z-40 w-72 transform border-r border-slate-200 bg-white transition-transform duration-300 ease-in-out lg:relative lg:translate-x-0 flex flex-col shadow-lg lg:shadow-none",
        isSidebarOpen ? "translate-x-0" : "-translate-x-full"
      )}>
        <div className="flex items-center justify-between p-5 border-b border-slate-100 bg-green-50/50">
          <div className="flex items-center gap-2">
            <Tractor className="text-green-600" size={24} />
            <h2 className="text-xl font-bold text-green-800">Krishi Mitra</h2>
          </div>
          <button onClick={() => setIsSidebarOpen(false)} className="lg:hidden text-slate-400 hover:text-green-600 transition-colors">
            <X size={20} />
          </button>
        </div>

        <div className="p-4">
          <button 
            onClick={createNewChat}
            className="w-full flex items-center gap-2 bg-green-600 hover:bg-green-700 text-white rounded-xl py-3 px-4 transition-all font-semibold justify-center shadow-md hover:shadow-green-200 active:scale-[0.98]"
          >
            <PlusCircle size={18} /> नई चर्चा (New Chat)
          </button>
        </div>

        <div className="flex-1 overflow-y-auto px-4 py-2 space-y-1">
          <p className="text-[11px] font-bold text-slate-400 uppercase tracking-wider mb-2 mt-2 px-2">History</p>
          {sessions.length === 0 && (
            <div className="text-slate-400 text-sm text-center py-6 italic">No chats yet</div>
          )}
          {sessions.map(s => (
            <div key={s.session_id} className="relative group">
              <button
                onClick={() => loadHistory(s.session_id)}
                className={clsx(
                  "w-full flex items-center justify-between px-3 py-3 rounded-xl text-sm text-left transition-all border",
                  activeSessionId === s.session_id 
                    ? "bg-green-50 border-green-200 text-green-700 font-medium" 
                    : "bg-transparent border-transparent text-slate-600 hover:bg-slate-50 hover:text-slate-900"
                )}
              >
                <div className="flex items-center gap-3 overflow-hidden pr-6">
                  <MessageSquare size={16} className={clsx("shrink-0", activeSessionId === s.session_id ? "text-green-600" : "text-slate-400")} />
                  <span className="truncate">{s.title || "Chat Session"}</span>
                </div>
              </button>
              <button 
                onClick={(e) => deleteChat(s.session_id, e)}
                className="absolute right-2 top-1/2 -translate-y-1/2 p-2 text-red-400 hover:text-red-600 hover:bg-red-50 rounded-lg opacity-0 group-hover:opacity-100 transition-all"
                title="Delete Chat"
              >
                <Trash2 size={14} />
              </button>
            </div>
          ))}
        </div>

        <div className="mt-auto border-t border-slate-100 p-4 space-y-4 bg-slate-50/50">
          <div>
            <label className="text-[10px] font-bold text-slate-400 mb-1 block uppercase">Language</label>
            <select 
              value={language}
              onChange={(e) => setLanguage(e.target.value)}
              className="w-full bg-white border border-slate-200 rounded-lg px-3 py-2 text-sm outline-none focus:border-green-500 shadow-sm"
            >
              <option value="English">English</option>
              <option value="Marathi">Marathi (मराठी)</option>
            </select>
          </div>
          
          <div className="p-3 bg-white border border-slate-200 rounded-xl shadow-sm">
            <div className="flex items-center gap-2 mb-1">
              <div className="w-8 h-8 rounded-full bg-green-100 flex items-center justify-center text-green-700">
                <User size={16} />
              </div>
              <div className="flex flex-col">
                <span className="text-sm font-bold text-slate-800 leading-none">{user.name}</span>
                <span className="text-[10px] text-slate-400 font-medium uppercase mt-0.5">District: {user.district}</span>
              </div>
            </div>
          </div>

          <button 
            onClick={onLogout}
            className="w-full flex items-center justify-center gap-2 text-sm font-bold text-red-500 hover:text-red-600 py-2.5 hover:bg-red-50 rounded-xl transition-all border border-transparent hover:border-red-100"
          >
            <LogOut size={16} /> Logout
          </button>
        </div>
      </div>

      {/* MOBILE OVERLAY */}
      {isSidebarOpen && (
        <div className="fixed inset-0 bg-slate-900/40 backdrop-blur-sm z-30 lg:hidden" onClick={() => setIsSidebarOpen(false)} />
      )}

      {/* MAIN CHAT */}
      <div className="flex-1 flex flex-col h-full bg-white">
        
        {/* HEADER */}
        <header className="flex items-center justify-between p-4 border-b border-white/40 bg-white/60 backdrop-blur-md sticky top-0 z-20 premium-shadow">
          <button onClick={() => setIsSidebarOpen(true)} className="lg:hidden text-green-700 p-2 bg-green-50 hover:bg-green-100 rounded-xl transition-colors">
            <Menu size={24} />
          </button>
          <div className="flex flex-col items-center flex-1">
             <div className="font-extrabold text-xl text-green-800 tracking-tight">Krishi Mitra AI</div>
             <div className="flex items-center gap-1.5 text-[11px] text-emerald-600 font-bold uppercase tracking-widest">
               <span className="w-2 h-2 rounded-full bg-emerald-500 animate-pulse shadow-[0_0_8px_rgba(16,185,129,0.6)]"></span> System Ready
             </div>
          </div>
          <div className="w-10 lg:hidden"></div>
        </header>

        {/* CHAT MESSAGES */}
        <div className="flex-1 overflow-y-auto p-4 md:p-6 space-y-8 scroll-smooth bg-slate-50/50">
          <div className="max-w-4xl mx-auto space-y-8">
            <AnimatePresence initial={false}>
              {messages.map((msg, i) => (
                <motion.div 
                  key={i}
                  initial={{ opacity: 0, y: 20, scale: 0.95 }}
                  animate={{ opacity: 1, y: 0, scale: 1 }}
                  transition={{ duration: 0.4, type: "spring", stiffness: 220, damping: 20 }}
                  className={clsx(
                    "flex flex-col gap-2 w-full",
                    msg.role === 'user' ? "items-end pl-12" : "items-start pr-4 md:pr-12"
                  )}
                >
                  {/* User Label */}
                  {msg.role === 'user' && (
                    <span className="text-[11px] font-bold text-green-700/60 mb-1 mr-3 uppercase tracking-wider">You</span>
                  )}
                  {msg.role === 'assistant' && (
                    <span className="text-[11px] font-bold text-emerald-700/60 mb-1 ml-3 uppercase tracking-wider">Krishi AI</span>
                  )}

                  {/* THINKING PROCESS (INSIDE THE BOX) */}
                  {msg.role === 'assistant' && msg.reasoning && (
                    <ReasoningBlock 
                      content={msg.reasoning} 
                      isStreaming={msg.isStreaming} 
                      hasAnswer={Boolean(msg.content)} 
                    />
                  )}

                  {/* THE COMPLETE ANSWER (OUTSIDE THE BOX) */}
                  {(msg.role === 'user' || msg.content || (msg.isStreaming && !msg.reasoning)) && (
                    <div className={clsx(
                      "px-6 py-4 rounded-3xl text-[16px] leading-relaxed md:text-[17px] min-w-[70px] transition-all",
                      msg.role === 'user' 
                        ? "bg-gradient-to-br from-green-500 to-emerald-600 text-white rounded-tr-sm shadow-xl shadow-green-600/20" 
                        : "bg-white border border-slate-100 text-slate-800 rounded-tl-sm shadow-xl shadow-slate-200/50"
                    )}>
                      {msg.role === 'assistant' && msg.isStreaming && !msg.content ? (
                         <div className="flex gap-1.5 py-2 px-1">
                           <span className="w-2.5 h-2.5 bg-emerald-500 rounded-full animate-bounce"></span>
                           <span className="w-2.5 h-2.5 bg-emerald-500 rounded-full animate-bounce" style={{ animationDelay: '150ms' }}></span>
                           <span className="w-2.5 h-2.5 bg-emerald-500 rounded-full animate-bounce" style={{ animationDelay: '300ms' }}></span>
                         </div>
                      ) : (
                        renderFormattedText(msg.content, false)
                      )}
                      
                      {msg.role === 'assistant' && msg.isStreaming && msg.content && (
                        <span className="inline-block w-2.5 h-5 ml-1 bg-emerald-500 animate-pulse align-middle rounded-sm"></span>
                      )}
                    </div>
                  )}
                </motion.div>
              ))}
            </AnimatePresence>
            <div ref={messagesEndRef} className="h-2" />
          </div>
        </div>

        {/* INPUT AREA */}
        <div className="p-4 border-t border-slate-100 bg-white">
          <div className="max-w-3xl mx-auto">
            <div className="relative flex items-center gap-3">
              <div className="flex-1 relative">
                <textarea
                  rows="1"
                  value={input}
                  onChange={(e) => setInput(e.target.value)}
                  onKeyDown={(e) => {
                    if (e.key === 'Enter' && !e.shiftKey) {
                      e.preventDefault();
                      handleSubmit();
                    }
                  }}
                  placeholder="खेती के बारे में पूछें... (Ask about farming...)"
                  className="w-full bg-slate-50 border border-slate-200 rounded-2xl px-5 py-4 outline-none focus:border-green-500 focus:bg-white focus:ring-4 focus:ring-green-100 transition-all resize-none overflow-hidden min-h-[60px] max-h-40 text-slate-800 text-[16px]"
                />
              </div>
              <button
                onClick={handleSubmit}
                disabled={!input.trim() || isGenerating}
                className="h-[60px] w-[60px] shrink-0 bg-green-600 hover:bg-green-700 disabled:bg-slate-200 disabled:text-slate-400 text-white rounded-2xl flex items-center justify-center transition-all shadow-lg shadow-green-100 hover:shadow-green-200 active:scale-95"
              >
                <Send size={24} />
              </button>
            </div>
            <div className="text-center mt-3">
              <span className="text-[11px] font-bold text-slate-400 uppercase tracking-tighter">Powered by Krishi AI - Helpful & Accurate Advice</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

function ReasoningBlock({ content, isStreaming, hasAnswer }) {
  const [isOpen, setIsOpen] = useState(false);
  
  useEffect(() => {
    if (hasAnswer && isStreaming) setIsOpen(false);
    if (isStreaming && !hasAnswer) setIsOpen(true);
  }, [hasAnswer, isStreaming]);

  const cleanContent = content.replace(/<tool_call>.*?<\/tool_call>/gs, '').trim();
  
  // If stream dies and we have nothing visible, keep the box alive to show an error or state
  if (!cleanContent && !isStreaming && !hasAnswer) {
    return (
      <div className="w-full mb-2 max-w-[95%] text-left text-red-500 text-xs font-bold pl-2">
        [Connection to AI Server Interrupted]
      </div>
    );
  }
  
  if (!cleanContent && !isStreaming) return null;

  return (
    <div className="w-full mb-2 max-w-[95%] text-left">
      <button 
        onClick={() => setIsOpen(!isOpen)}
        className={clsx(
          "w-full flex items-center justify-between px-5 py-3.5 text-[12px] font-bold border transition-all rounded-2xl",
          isOpen 
            ? "bg-slate-50/80 border-slate-200/60 text-slate-600 rounded-b-none" 
            : "bg-white border-slate-200/60 text-slate-500 shadow-sm hover:border-slate-300 hover:shadow-md"
        )}
      >
        <div className="flex items-center gap-3">
          <div className={clsx(
            "p-1.5 rounded-lg transition-colors",
            isStreaming ? "bg-emerald-100 text-emerald-600 shadow-[0_0_10px_rgba(16,185,129,0.3)]" : "bg-slate-100 text-slate-400"
          )}>
            <BrainCircuit size={16} className={isStreaming ? "animate-spin-slow" : ""} />
          </div>
          <span className="uppercase tracking-widest leading-none mt-0.5">
            {isStreaming ? (hasAnswer ? "Finalizing Response..." : "AI Thinking...") : "Thinking Process Completed"}
          </span>
        </div>
        <div className={clsx("p-1 rounded-full transition-colors", isOpen ? "bg-slate-200" : "bg-slate-50")}>
          {isOpen ? <ChevronUp size={16} /> : <ChevronDown size={16} />}
        </div>
      </button>
      
      <AnimatePresence>
        {isOpen && (
          <motion.div 
            initial={{ height: 0, opacity: 0 }}
            animate={{ height: "auto", opacity: 1 }}
            exit={{ height: 0, opacity: 0 }}
            className="overflow-hidden border border-t-0 border-slate-200/60 rounded-b-2xl shadow-sm bg-slate-50/50 backdrop-blur-sm"
          >
            <div className="p-5 text-[14px] text-slate-600 leading-relaxed italic border-l-4 border-l-slate-300/80 m-2 rounded-r-lg">
              {renderFormattedText(cleanContent || "Operating internal tools...", true)}
              {isStreaming && <span className="inline-block w-2.5 h-2.5 ml-2 bg-emerald-400 rounded-full animate-pulse shadow-[0_0_8px_rgba(52,211,153,0.8)]"></span>}
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
}
