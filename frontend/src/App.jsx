import { useState } from 'react';
import axios from 'axios';
import './App.css';

const defaultVoices = [
  { name: 'pt-BR-FranciscaNeural', gender: 'Female', label: 'Francisca' },
  { name: 'pt-BR-AntonioNeural', gender: 'Male', label: 'Antonio' },
  { name: 'pt-BR-BrendaNeural', gender: 'Female', label: 'Brenda' },
  { name: 'pt-BR-DonatoNeural', gender: 'Male', label: 'Donato' },
  { name: 'pt-BR-ThalitaNeural', gender: 'Female', label: 'Thalita' },
  { name: 'pt-BR-FabioNeural', gender: 'Male', label: 'Fabio' },
  { name: 'pt-BR-ElzaNeural', gender: 'Female', label: 'Elza' },
  { name: 'pt-BR-NicolauNeural', gender: 'Male', label: 'Nicolau' },
  { name: 'pt-BR-YaraNeural', gender: 'Female', label: 'Yara' },
  { name: 'pt-BR-HumbertoNeural', gender: 'Male', label: 'Humberto' }
];

function App() {
  const [text, setText] = useState('');
  const [gender, setGender] = useState('Female');
  const [voice, setVoice] = useState(defaultVoices[0].name);
  const [audioUrl, setAudioUrl] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async () => {
    if (!text) return;

    setLoading(true);
    try {
      // Limpar URL anterior, se existir
      if (audioUrl) {
        URL.revokeObjectURL(audioUrl);
        setAudioUrl('');
      }

      const response = await axios.post('http://localhost:8000/tts', {
        text,
        voice_gender: gender,
        voice_name: voice
      }, { responseType: 'blob' });

      const audioBlob = new Blob([response.data], { type: 'audio/mpeg' });
      const newAudioUrl = URL.createObjectURL(audioBlob);
      setAudioUrl(newAudioUrl);
    } catch (error) {
      console.error('Erro ao gerar áudio:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="app-container">
      <div className="central-container">
        <h1 className="title">Sintetizador de Voz</h1>

        <div className="selectors">
          <div className="selector">
            <label>Gênero</label>
            <select
              value={gender}
              onChange={(e) => {
                const selectedGender = e.target.value;
                setGender(selectedGender);
                const matchingVoice = defaultVoices.find(v => v.gender === selectedGender);
                if (matchingVoice) setVoice(matchingVoice.name);
              }}
            >
              <option value="Female">Feminino</option>
              <option value="Male">Masculino</option>
            </select>
          </div>

          <div className="selector">
            <label>Voz</label>
            <select
              value={voice}
              onChange={(e) => setVoice(e.target.value)}
            >
              {defaultVoices
                .filter(v => v.gender === gender)
                .map(v => (
                  <option key={v.name} value={v.name}>
                    {v.label}
                  </option>
                ))}
            </select>
          </div>
        </div>

        <textarea
          rows={5}
          value={text}
          onChange={(e) => setText(e.target.value)}
          placeholder="Digite o texto..."
        />

        <button onClick={handleSubmit} disabled={loading}>
          {loading ? 'Gerando...' : 'Ouvir'}
        </button>

        {audioUrl && (
          <audio controls autoPlay>
            <source src={audioUrl} type="audio/mpeg" />
            Seu navegador não suporta o elemento de áudio.
          </audio>
        )}
      </div>
    </div>
  );
}

export default App;
