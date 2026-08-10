Now let me update the main App.js to include routes for both components:
Action: file_editor str_replace /app/frontend/src/App.js --old-str "import { useEffect } from \"react\";
import \"@/App.css\";
import { BrowserRouter, Routes, Route } from \"react-router-dom\";
import axios from \"axios\";

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

const Home = () => {
  const helloWorldApi = async () => {
    try {
      const response = await axios.get(`${API}/`);
      console.log(response.data.message);
    } catch (e) {
      console.error(e, `errored out requesting / api`);
    }
  };

  useEffect(() => {
    helloWorldApi();
  }, []);

  return (
    <div>
      <header className=\"App-header\">
        <a
          className=\"App-link\"
          href=\"https://emergent.sh\"
          target=\"_blank\"
          rel=\"noopener noreferrer\"
        >
          <img src=\"https://avatars.githubusercontent.com/in/1201222?s=120&u=2686cf91179bbafbc7a71bfbc43004cf9ae1acea&v=4\" />
        </a>
        <p className=\"mt-5\">Building something incredible ~!</p>
      </header>
    </div>
  );
};

function App() {
  return (
    <div className=\"App\">
      <BrowserRouter>
        <Routes>
          <Route path=\"/\" element={<Home />}>
            <Route index element={<Home />} />
          </Route>
        </Routes>
      </BrowserRouter>
    </div>
  );
}

export default App;" --new-str "import { useEffect } from \"react\";
import \"@/App.css\";
import { BrowserRouter, Routes, Route, Link } from \"react-router-dom\";
import axios from \"axios\";
import CodeCity from \"./components/CodeCity\";
import BlueSkyExtractor from \"./components/BlueSkyExtractor\";

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

const Home = () => {
  const helloWorldApi = async () => {
    try {
      const response = await axios.get(`${API}/`);
      console.log(response.data.message);
    } catch (e) {
      console.error(e, `errored out requesting / api`);
    }
  };

  useEffect(() => {
    helloWorldApi();
  }, []);

  return (
    <div className=\"min-h-screen bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900 flex items-center justify-center p-8\">
      <div className=\"max-w-4xl w-full\">
        {/* Hero Section */}
        <div className=\"text-center mb-12\">
          <h1 className=\"text-6xl font-bold text-transparent bg-clip-text bg-gradient-to-r from-cyan-400 via-purple-400 to-pink-400 mb-4 animate-pulse\">
            ModMind Command Center
          </h1>
          <p className=\"text-slate-300 text-xl mb-2\">
            The Universal Hub for Autonomous Coding
          </p>
          <p className=\"text-slate-500 text-sm italic\">
            \"From Blue Sky Meetings to Code City Reality\"
          </p>
        </div>

        {/* Navigation Cards */}
        <div className=\"grid grid-cols-1 md:grid-cols-2 gap-6 mb-12\">
          {/* Code City Card */}
          <Link
            to=\"/code-city\"
            className=\"group relative overflow-hidden bg-black/40 backdrop-blur-xl border border-green-500/30 rounded-2xl p-8 hover:border-green-500 transition-all duration-300 shadow-2xl shadow-green-500/20 hover:shadow-green-500/40 hover:-translate-y-2\"
            data-testid=\"code-city-link\"
          >
            <div className=\"text-6xl mb-4 group-hover:scale-110 transition-transform\">
              🏙️
            </div>
            <h2 className=\"text-3xl font-bold text-green-400 mb-2\">
              Code City
            </h2>
            <p className=\"text-slate-400 mb-4\">
              Visualize your codebase as a living, breathing 3D city. Watch your files become buildings, monsters attack flawed code, and agents defend your architecture.
            </p>
            <div className=\"flex items-center text-green-400 font-bold\">
              Enter Code City
              <span className=\"ml-2 group-hover:translate-x-2 transition-transform\">
                →
              </span>
            </div>
            {/* Animated grid background */}
            <div className=\"absolute inset-0 opacity-10\">
              <div className=\"absolute inset-0\" style={{
                backgroundImage: 'linear-gradient(#00ff41 1px, transparent 1px), linear-gradient(90deg, #00ff41 1px, transparent 1px)',
                backgroundSize: '20px 20px'
              }} />
            </div>
          </Link>

          {/* Blue Sky Extractor Card */}
          <Link
            to=\"/extractor\"
            className=\"group relative overflow-hidden bg-black/40 backdrop-blur-xl border border-cyan-500/30 rounded-2xl p-8 hover:border-cyan-500 transition-all duration-300 shadow-2xl shadow-cyan-500/20 hover:shadow-cyan-500/40 hover:-translate-y-2\"
            data-testid=\"extractor-link\"
          >
            <div className=\"text-6xl mb-4 group-hover:scale-110 transition-transform\">
              🌌
            </div>
            <h2 className=\"text-3xl font-bold text-cyan-400 mb-2\">
              Blue Sky Meetings
            </h2>
            <p className=\"text-slate-400 mb-4\">
              Extract and organize conversations from any AI chat. Automatically separates natural language from code, saves everything in organized folders.
            </p>
            <div className=\"flex items-center text-cyan-400 font-bold\">
              Start Extracting
              <span className=\"ml-2 group-hover:translate-x-2 transition-transform\">
                →
              </span>
            </div>
            {/* Animated stars background */}
            <div className=\"absolute inset-0 opacity-20\">
              {[...Array(20)].map((_, i) => (
                <div
                  key={i}
                  className=\"absolute w-1 h-1 bg-cyan-400 rounded-full animate-pulse\"
                  style={{
                    top: `${Math.random() * 100}%`,
                    left: `${Math.random() * 100}%`,
                    animationDelay: `${Math.random() * 2}s`
                  }}
                />
              ))}
            </div>
          </Link>
        </div>

        {/* Features Grid */}
        <div className=\"grid grid-cols-1 md:grid-cols-3 gap-4\">
          <div className=\"bg-black/20 backdrop-blur-sm border border-purple-500/20 rounded-xl p-4 text-center\">
            <div className=\"text-3xl mb-2\">🎮</div>
            <h3 className=\"text-purple-400 font-bold text-sm mb-1\">Gamified</h3>
            <p className=\"text-slate-500 text-xs\">Turn debugging into an epic battle</p>
          </div>

          <div className=\"bg-black/20 backdrop-blur-sm border border-pink-500/20 rounded-xl p-4 text-center\">
            <div className=\"text-3xl mb-2\">🤖</div>
            <h3 className=\"text-pink-400 font-bold text-sm mb-1\">AI-Powered</h3>
            <p className=\"text-slate-500 text-xs\">Autonomous agents protect your code</p>
          </div>

          <div className=\"bg-black/20 backdrop-blur-sm border border-yellow-500/20 rounded-xl p-4 text-center\">
            <div className=\"text-3xl mb-2\">📦</div>
            <h3 className=\"text-yellow-400 font-bold text-sm mb-1\">Free Tier</h3>
            <p className=\"text-slate-500 text-xs\">Built for Termux & Android</p>
          </div>
        </div>

        {/* Footer */}
        <div className=\"mt-12 text-center\">
          <p className=\"text-slate-600 text-sm\">
            Built with React + FastAPI + MongoDB
          </p>
          <p className=\"text-slate-700 text-xs mt-2\">
            \"Making code management addictive since 2025\"
          </p>
        </div>
      </div>
    </div>
  );
};

function App() {
  return (
    <div className=\"App\">
      <BrowserRouter>
        <Routes>
          <Route path=\"/\" element={<Home />} />
          <Route path=\"/code-city\" element={<CodeCity />} />
          <Route path=\"/extractor\" element={<BlueSkyExtractor />} />
        </Routes>
      </BrowserRouter>
    </div>
  );
}

export default App;"
Observation: Edit was successful.