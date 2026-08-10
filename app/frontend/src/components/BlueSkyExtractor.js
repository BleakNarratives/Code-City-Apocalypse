Now let me create the Chat Extractor component:
Action: file_editor create /app/frontend/src/components/BlueSkyExtractor.js --file-text "import React, { useState, useEffect } from 'react';
import axios from 'axios';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

const BlueSkyExtractor = () => {
  const [message, setMessage] = useState('');
  const [modelName, setModelName] = useState('Claude');
  const [sessionId, setSessionId] = useState('');
  const [sessions, setSessions] = useState([]);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    loadSessions();
  }, []);

  const loadSessions = async () => {
    try {
      const response = await axios.get(`${API}/sessions`);
      setSessions(response.data.sessions);
    } catch (error) {
      console.error('Error loading sessions:', error);
    }
  };

  const extractChat = async () => {
    if (!message.trim()) {
      alert('Please paste a chat message');
      return;
    }

    setLoading(true);
    try {
      const response = await axios.post(`${API}/extract-chat`, {
        message,
        model_name: modelName,
        session_id: sessionId || null
      });
      setResult(response.data);
      setMessage(''); // Clear after successful extraction
      loadSessions(); // Refresh session list
    } catch (error) {
      console.error('Error extracting chat:', error);
      alert('Error extracting chat. Check console for details.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className=\"min-h-screen bg-gradient-to-br from-slate-900 via-indigo-900 to-slate-900 p-8\">
      <div className=\"max-w-6xl mx-auto\">
        {/* Header */}
        <div className=\"mb-8 text-center\">
          <h1 className=\"text-5xl font-bold text-transparent bg-clip-text bg-gradient-to-r from-cyan-400 to-blue-400 mb-2\">
            🌌 Blue Sky Meeting Extractor
          </h1>
          <p className=\"text-slate-400 text-lg\">
            Extract natural language and code from any AI chat
          </p>
        </div>

        <div className=\"grid grid-cols-1 lg:grid-cols-2 gap-6\">
          {/* Input Panel */}
          <div className=\"bg-black/40 backdrop-blur-xl border border-cyan-500/30 rounded-2xl p-6 shadow-2xl shadow-cyan-500/20\">
            <h2 className=\"text-2xl font-bold text-cyan-400 mb-4\">
              📝 Chat Input
            </h2>

            {/* Model Selection */}
            <div className=\"mb-4\">
              <label className=\"block text-slate-300 text-sm mb-2\">
                AI Model:
              </label>
              <select
                value={modelName}
                onChange={(e) => setModelName(e.target.value)}
                className=\"w-full bg-black/60 border border-cyan-500/30 text-cyan-300 px-4 py-3 rounded-lg focus:outline-none focus:border-cyan-500\"
                data-testid=\"model-select\"
              >
                <option value=\"Claude\">Claude</option>
                <option value=\"GPT-4\">GPT-4</option>
                <option value=\"GPT-3.5\">GPT-3.5</option>
                <option value=\"Gemini\">Gemini</option>
                <option value=\"Perplexity\">Perplexity</option>
                <option value=\"Other\">Other</option>
              </select>
            </div>

            {/* Session ID */}
            <div className=\"mb-4\">
              <label className=\"block text-slate-300 text-sm mb-2\">
                Session ID (optional):
              </label>
              <input
                type=\"text\"
                value={sessionId}
                onChange={(e) => setSessionId(e.target.value)}
                placeholder=\"Leave blank for auto-generated\"
                className=\"w-full bg-black/60 border border-cyan-500/30 text-cyan-300 px-4 py-3 rounded-lg focus:outline-none focus:border-cyan-500\"
                data-testid=\"session-id-input\"
              />
            </div>

            {/* Message Input */}
            <div className=\"mb-4\">
              <label className=\"block text-slate-300 text-sm mb-2\">
                Paste Chat Message:
              </label>
              <textarea
                value={message}
                onChange={(e) => setMessage(e.target.value)}
                placeholder=\"Paste your entire chat conversation here...\"
                rows={12}
                className=\"w-full bg-black/60 border border-cyan-500/30 text-cyan-300 px-4 py-3 rounded-lg focus:outline-none focus:border-cyan-500 font-mono text-sm\"
                data-testid=\"message-input\"
              />
            </div>

            {/* Extract Button */}
            <button
              onClick={extractChat}
              disabled={loading || !message.trim()}
              className=\"w-full bg-gradient-to-r from-cyan-500 to-blue-500 text-white px-6 py-4 rounded-lg font-bold text-lg hover:from-cyan-600 hover:to-blue-600 transition-all disabled:opacity-50 disabled:cursor-not-allowed shadow-lg shadow-cyan-500/50\"
              data-testid=\"extract-button\"
            >
              {loading ? '⏳ Extracting...' : '✨ Extract & Save'}
            </button>
          </div>

          {/* Result Panel */}
          <div className=\"space-y-6\">
            {/* Latest Result */}
            {result && (
              <div className=\"bg-black/40 backdrop-blur-xl border border-green-500/30 rounded-2xl p-6 shadow-2xl shadow-green-500/20\">
                <h2 className=\"text-2xl font-bold text-green-400 mb-4\">
                  ✅ Extraction Complete
                </h2>

                <div className=\"space-y-3 text-sm\">
                  <div className=\"flex justify-between items-center p-3 bg-black/40 rounded-lg\">
                    <span className=\"text-slate-400\">Session ID:</span>
                    <span className=\"text-yellow-400 font-mono\">{result.session_id}</span>
                  </div>

                  <div className=\"flex justify-between items-center p-3 bg-black/40 rounded-lg\">
                    <span className=\"text-slate-400\">Model:</span>
                    <span className=\"text-blue-400 font-bold\">{result.model}</span>
                  </div>

                  <div className=\"flex justify-between items-center p-3 bg-black/40 rounded-lg\">
                    <span className=\"text-slate-400\">Code Blocks Found:</span>
                    <span className=\"text-purple-400 font-bold\">{result.stats.code_blocks_found}</span>
                  </div>

                  <div className=\"flex justify-between items-center p-3 bg-black/40 rounded-lg\">
                    <span className=\"text-slate-400\">Natural Language Chars:</span>
                    <span className=\"text-cyan-400 font-bold\">{result.stats.natural_language_chars}</span>
                  </div>

                  <div className=\"p-3 bg-black/40 rounded-lg\">
                    <span className=\"text-slate-400 block mb-2\">Natural Language File:</span>
                    <span className=\"text-green-400 font-mono text-xs break-all\">
                      {result.natural_language_file}
                    </span>
                  </div>

                  {result.code_files.length > 0 && (
                    <div className=\"p-3 bg-black/40 rounded-lg\">
                      <span className=\"text-slate-400 block mb-2\">Code Files:</span>
                      <div className=\"space-y-1\">
                        {result.code_files.map((file, idx) => (
                          <div key={idx} className=\"text-purple-400 font-mono text-xs break-all\">
                            {file}
                          </div>
                        ))}
                      </div>
                    </div>
                  )}
                </div>
              </div>
            )}

            {/* Sessions List */}
            <div className=\"bg-black/40 backdrop-blur-xl border border-purple-500/30 rounded-2xl p-6 shadow-2xl shadow-purple-500/20\">
              <h2 className=\"text-2xl font-bold text-purple-400 mb-4 flex items-center justify-between\">
                <span>📚 Recent Sessions</span>
                <button
                  onClick={loadSessions}
                  className=\"text-sm bg-purple-500/20 px-3 py-1 rounded hover:bg-purple-500/40 transition-all\"
                  data-testid=\"refresh-sessions-button\"
                >
                  🔄
                </button>
              </h2>

              <div className=\"space-y-2 max-h-96 overflow-y-auto\">
                {sessions.length === 0 ? (
                  <p className=\"text-slate-500 text-center py-8\">
                    No sessions yet. Start extracting!
                  </p>
                ) : (
                  sessions.map((session, idx) => (
                    <div
                      key={idx}
                      className=\"p-3 bg-black/40 rounded-lg border border-purple-500/20 hover:border-purple-500/40 transition-all cursor-pointer\"
                      data-testid={`session-${idx}`}
                    >
                      <div className=\"flex justify-between items-center mb-1\">
                        <span className=\"text-yellow-400 font-bold text-sm\">
                          📅 {session.date}
                        </span>
                        <span className=\"text-blue-400 font-mono text-xs\">
                          {session.model}
                        </span>
                      </div>
                      <div className=\"text-slate-500 font-mono text-xs\">
                        {session.path}
                      </div>
                    </div>
                  ))
                )}
              </div>
            </div>
          </div>
        </div>

        {/* Info Cards */}
        <div className=\"mt-8 grid grid-cols-1 md:grid-cols-3 gap-4\">
          <div className=\"bg-gradient-to-br from-cyan-500/10 to-blue-500/10 border border-cyan-500/30 rounded-xl p-4\">
            <div className=\"text-3xl mb-2\">🧹</div>
            <h3 className=\"text-cyan-400 font-bold mb-1\">Clean Extraction</h3>
            <p className=\"text-slate-400 text-sm\">
              Removes all code blocks, saves pure natural language
            </p>
          </div>

          <div className=\"bg-gradient-to-br from-purple-500/10 to-pink-500/10 border border-purple-500/30 rounded-xl p-4\">
            <div className=\"text-3xl mb-2\">📁</div>
            <h3 className=\"text-purple-400 font-bold mb-1\">Auto-Organized</h3>
            <p className=\"text-slate-400 text-sm\">
              Files saved in date/model folder structure
            </p>
          </div>

          <div className=\"bg-gradient-to-br from-green-500/10 to-emerald-500/10 border border-green-500/30 rounded-xl p-4\">
            <div className=\"text-3xl mb-2\">⚡</div>
            <h3 className=\"text-green-400 font-bold mb-1\">Code Ready</h3>
            <p className=\"text-slate-400 text-sm\">
              Code blocks saved separately with correct extensions
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default BlueSkyExtractor;
"
Observation: Create successful: /app/frontend/src/components/BlueSkyExtractor.js