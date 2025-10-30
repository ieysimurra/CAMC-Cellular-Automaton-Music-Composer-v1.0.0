# ⚡ Quick Start Guide

Get up and running with CA Music Composer in 5 minutes!

[🇧🇷 Português](docs/QUICKSTART_PT.md) | [🇺🇸 English](docs/QUICKSTART.md)

---

## 🚀 Fastest Way to Try (Web)

### Option 1: Use Online Demo (No Installation!)

👉 **[Try Now](https://ca-music-composer.streamlit.app)** _(replace with actual URL)_

No installation needed! Just open and start composing.

---

### Option 2: Run Locally (5 minutes)

```bash
# 1. Clone
git clone https://github.com/your-username/ca-music-composer.git
cd ca-music-composer

# 2. Install
pip install -r requirements-streamlit.txt

# 3. Run
streamlit run CA-poly-instrument-11-streamlit.py

# Done! Opens at http://localhost:8501
```

---

## 🎵 Create Your First Composition (3 Steps)

### Step 1: Select Instruments (30 seconds)

```
1. Choose "Violin" - Set quantity to 1
2. Choose "Cello" - Set quantity to 1
3. Click "Confirm Selection"
```

### Step 2: Configure (1 minute)

**For each instrument**, use these simple settings:

```yaml
Violin:
  Generations: 40
  States: 8
  Rule: Deterministic
  Initial Note: G
  Octaves: [4, 5]
  
Cello:
  Generations: 40
  States: 6
  Rule: Deterministic
  Initial Note: C
  Octaves: [2, 3]
```

Click **"Generate CA"** for both instruments.

### Step 3: Export (30 seconds)

```
1. Click "Generate Score"
2. Go to "MIDI" tab
3. Click "Download MIDI"
4. Open with VLC or your favorite player
5. Enjoy your first CA composition! 🎉
```

**Total time:** ~3 minutes

---

## 📖 Next Steps

Now that you've created your first piece:

1. 🎨 **Experiment with different rules**
   - Try "Random" for unpredictable music
   - Try "Mathematical" with formula: `(state * 2) % num_states`

2. 🎼 **Add more instruments**
   - Create a full string quartet (2 Violins + Viola + Cello)
   - Try wind instruments (Flute, Clarinet)

3. 📚 **Read the full tutorial**
   - [Complete Tutorial](docs/TUTORIAL.md)
   - [FAQ](docs/FAQ.md)

4. 🎵 **Check out examples**
   - [Example Compositions](examples/)
   - [Video Tutorials](https://youtube.com/...)

---

## 💡 Pro Tips

### Tip 1: Start Simple
- Begin with 1-2 instruments
- Use 8 states (not too many)
- Stick with "Deterministic" rule first

### Tip 2: Use Recommended Settings

| Instrument | Octaves | States |
|------------|---------|--------|
| Flute | [5, 6] | 10-12 |
| Violin | [4, 5] | 8-10 |
| Viola | [3, 4] | 8 |
| Cello | [2, 3] | 6-8 |
| Bass | [1, 2] | 4-6 |

### Tip 3: Visualize Before Creating Score
Always click "Generate CA" and **check the heatmap** before creating the score. If it looks too random or too regular, adjust parameters.

---

## 🆘 Common Issues

### "Module not found"
```bash
pip install -r requirements-streamlit.txt
```

### "MIDI has no sound"
Use VLC Media Player (free): [videolan.org](https://www.videolan.org/)

### "Application won't start"
```bash
# Check Python version (need 3.8+)
python --version

# If < 3.8, upgrade Python
```

---

## 🎓 Learning Path

**Beginner (Week 1)**
1. ✅ Quick Start (this guide)
2. 📖 Read Tutorial sections 1-3
3. 🎵 Create 3-5 simple compositions

**Intermediate (Week 2-3)**
1. 🎨 Try all 5 rule types
2. 🎼 Create multi-instrument pieces
3. 📝 Read FAQ and best practices

**Advanced (Week 4+)**
1. 🧮 Create custom mathematical rules
2. 🎺 Orchestral compositions
3. 🤝 Contribute to the project

---

## 📞 Get Help

- 💬 [GitHub Discussions](https://github.com/your-username/ca-music-composer/discussions)
- 📧 Email: your.email@example.com
- 📖 [Full Documentation](README.md)

---

## ⭐ Enjoying It?

- Star the repo on GitHub
- Share with friends
- Submit your compositions to our gallery
- Contribute improvements

---

<div align="center">

**Ready to create something amazing?**

[🚀 Launch App](https://ca-music-composer.streamlit.app) | [📖 Full Tutorial](docs/TUTORIAL.md)

</div>
