"""
🤖 NainoAcademy Bot – Enhanced Version
Python 3.14 + python-telegram-bot v13
"""

import random, html
import time
from datetime import datetime, timedelta
from telegram import (
    Update, InlineKeyboardButton, InlineKeyboardMarkup, ParseMode
)
from telegram.ext import (
    Updater, CommandHandler, CallbackContext,
    CallbackQueryHandler
)

# ---------------- CONFIG ----------------
BOT_TOKEN = "8250394638:AAEP0sHA0Rl-gj1NCyXc_-WKg1HV-GWAZTI"
ADMIN_USERNAME = "Nainoacademy"
COURSE_LINK = "https://nainoacademy.blogspot.com/"
HOW_TO_BUY_LINK = "https://youtube.com/shorts/zgEWUhCQsk0?si=mmFecsnGoLuaBzxP"
# ----------------------------------------

user_scores = {}
user_answered_questions = {}  # Track answered questions per user
user_cooldowns = {}  # Track cooldowns for daily challenge

# ---------------- DATA ----------------
QUIZ_LIST = [
    # Physics Questions (1-35)
    ("Which law explains the relationship between current and voltage?", 
     ["Ohm's Law", "Faraday's Law", "Ampere's Law", "Lenz's Law"], 0),
    ("The SI unit of power is:", ["Watt", "Joule", "Newton", "Pascal"], 0),
    ("Which of the following is not a conservative force?", 
     ["Gravitational force", "Electrostatic force", "Frictional force", "Spring force"], 2),
    ("The unit of Planck's constant is:", 
     ["Joule-second", "Joule/second", "Joule/metre", "Joule-meter"], 0),
    ("A body is falling freely under gravity. The kinetic energy of the body:", 
     ["Remains constant", "Increases linearly", "Decreases linearly", "Increases non-linearly"], 3),
    ("The dimensional formula for impulse is:", 
     ["[MLT⁻²]", "[ML²T⁻²]", "[MLT⁻¹]", "[M⁰L⁰T⁻¹]"], 2),
    ("At the highest point of a projectile's motion, the velocity is:", 
     ["Zero", "Maximum", "Equal to the initial velocity", "Minimum but not zero"], 3),
    ("The work done by a centripetal force acting on a body moving in a circle is:", 
     ["Always positive", "Always negative", "Zero", "None of these"], 2),
    ("According to Kepler's law of planetary motion, the square of the time period is proportional to the:", 
     ["Semi-major axis", "Square of the semi-major axis", "Cube of the semi-major axis", "Fourth power of the semi-major axis"], 2),
    ("The escape velocity from the surface of the Earth is:", 
     ["2 km/s", "8 km/s", "11.2 km/s", "16.7 km/s"], 2),
    ("A person sits on a chair with his feet on the ground. The action-reaction pair according to Newton's third law is:", 
     ["Weight of the person and the normal force by the ground", "Weight of the person and the normal force by the chair", "Force by the person on the chair and the normal force by the chair", "Gravitational force on the person and the gravitational force on the Earth by the person"], 3),
    ("The SI unit of electric potential is:", 
     ["Joule", "Volt", "Coulomb", "Ohm"], 1),
    ("The magnetic field inside a long solenoid is:", 
     ["Zero", "Uniform", "Non-uniform", "Circular"], 1),
    ("For a convex lens, the image is virtual and erect when the object is placed:", 
     ["At focus", "Between focus and optical centre", "At infinity", "Beyond 2F"], 1),
    ("The phenomenon of light used in optical fibers is:", 
     ["Refraction", "Dispersion", "Total Internal Reflection", "Scattering"], 2),
    ("In a p-n junction diode, the depletion region is due to:", 
     ["Doping of impurities", "Diffusion of charge carriers", "Drift of charge carriers", "Presence of surface charges"], 1),
    ("The half-life of a radioactive substance is 10 days. The mean life is approximately:", 
     ["6.93 days", "14.43 days", "10 days", "3.36 days"], 1),
    ("The energy of a photon of wavelength λ is:", 
     ["hcλ", "hλ/c", "hc/λ", "h/cλ"], 2),
    ("In a pure capacitive AC circuit, the voltage:", 
     ["Lags behind current by π/2", "Leads current by π/2", "Is in phase with current", "Lags behind current by π"], 0),
    ("The ratio of the radii of gyration of a circular disc and a circular ring of the same mass and radius about a tangential axis parallel to the plane is:", 
     ["1 : √2", "√2 : 1", "√3 : √2", "1 : 2"], 2),
    ("A capillary tube of radius 'r' is dipped in a liquid. The height of liquid that rises in the capillary is 'h'. If the radius is reduced to 'r/2', the height becomes:", 
     ["h/2", "h", "2h", "4h"], 2),
    ("The temperature at which the RMS velocity of oxygen molecules is equal to that of hydrogen molecules at 27°C is:", 
     ["27°C", "54°C", "327°C", "427°C"], 3),
    ("In a Young's double-slit experiment, if the separation between the slits is doubled, the fringe width becomes:", 
     ["Half", "Double", "One-fourth", "Four times"], 0),
    ("The de Broglie wavelength of an electron accelerated by a potential of V volts is given by:", 
     ["λ = 1.227/√V nm", "λ = 1.227/V nm", "λ = √(1.227/V) nm", "λ = 12.27/√V Å"], 0),
    ("A transformer works on the principle of:", 
     ["Self induction", "Mutual induction", "Eddy currents", "Electrical resonance"], 1),
    ("The torque on a dipole in a uniform electric field is maximum when the angle between p and E is:", 
     ["0°", "90°", "180°", "45°"], 1),
    ("A body of mass 2 kg is thrown vertically upward with a kinetic energy of 490 J. The height at which the kinetic energy becomes half of its initial value is (g=9.8 m/s²):", 
     ["12.5 m", "25 m", "10 m", "50 m"], 0),
    ("The law of floatation is based on:", 
     ["Archimedes' principle", "Pascal's law", "Bernoulli's theorem", "Hooke's law"], 0),
    ("The SI unit of luminous intensity is:", 
     ["Lumen", "Lux", "Candela", "Watt"], 2),
    ("In a common emitter configuration, the current gain is:", 
     ["α", "β", "γ", "1"], 1),
    ("The critical angle for a medium is 30°. Its refractive index is:", 
     ["1.5", "2.0", "2.5", "0.5"], 1),
    ("Which of the following is not a fundamental force?", 
     ["Gravitational force", "Electromagnetic force", "Nuclear force", "Frictional force"], 3),
    ("The process of emission of electrons from a metal surface when light falls on it is called:", 
     ["Photoelectric effect", "Compton effect", "Pair production", "Radioactivity"], 0),
    ("The unit of magnetic flux is:", 
     ["Tesla", "Weber", "Henry", "Gauss"], 1),
    ("According to Bohr's model, the angular momentum of an electron in nth orbit is:", 
     ["nh/2π", "2π/nh", "n²h/2π", "h/2πn"], 0),

    # Chemistry Questions (36-70)
    ("Which of the following has the highest electron affinity?", 
     ["Fluorine", "Chlorine", "Bromine", "Iodine"], 1),
    ("The IUPAC name of CH₃-CH₂-CO-CH₃ is:", 
     ["Butan-2-one", "Butan-1-one", "Pentan-2-one", "Pentan-3-one"], 0),
    ("The number of sigma (σ) and pi (π) bonds in ethene (C₂H₄) is:", 
     ["4 σ, 1 π", "5 σ, 1 π", "4 σ, 2 π", "5 σ, 2 π"], 1),
    ("The geometry of XeF₄ molecule is:", 
     ["Square planar", "Tetrahedral", "Square pyramidal", "Octahedral"], 0),
    ("The catalyst used in the Contact Process for the manufacture of sulfuric acid is:", 
     ["Fe", "V₂O₅", "Pt", "Ni"], 1),
    ("The law of triads was proposed by:", 
     ["Dobereiner", "Newlands", "Mendeleev", "Moseley"], 0),
    ("The hybridisation of carbon in diamond is:", 
     ["sp", "sp²", "sp³", "sp³d"], 2),
    ("Which of the following is an example of a lyophobic colloid?", 
     ["Starch solution", "Gum", "Blood", "Metal sol"], 3),
    ("The unit of rate constant for a zero-order reaction is:", 
     ["mol L⁻¹ s⁻¹", "s⁻¹", "L mol⁻¹ s⁻¹", "L² mol⁻² s⁻¹"], 0),
    ("According to Le Chatelier's principle, for an exothermic reaction, increase in temperature:", 
     ["Favors forward reaction", "Favors backward reaction", "No effect", "Increases the rate constant"], 1),
    ("The most electronegative element is:", 
     ["Fluorine", "Chlorine", "Oxygen", "Nitrogen"], 0),
    ("The number of periods in the modern periodic table is:", 
     ["7", "8", "18", "9"], 0),
    ("Which of the following is an intensive property?", 
     ["Mass", "Volume", "Refractive index", "Enthalpy"], 2),
    ("The oxidation state of chromium in K₂Cr₂O₇ is:", 
     ["+2", "+4", "+6", "+7"], 2),
    ("The process of converting nitrates to nitrogen gas is called:", 
     ["Nitrogen fixation", "Ammonification", "Nitrification", "Denitrification"], 3),
    ("Which of the following is not a greenhouse gas?", 
     ["CO₂", "CH₄", "N₂", "CFC"], 2),
    ("The pH of a neutral solution at 25°C is:", 
     ["0", "7", "14", "1"], 1),
    ("The hardest substance known is:", 
     ["Gold", "Iron", "Diamond", "Platinum"], 2),
    ("The molecular formula of benzene is:", 
     ["C₆H₆", "C₆H₁₂", "C₆H₁₀", "C₆H₈"], 0),
    ("Which of the following is a reducing sugar?", 
     ["Sucrose", "Glucose", "Maltose", "Both Glucose and Maltose"], 3),
    ("The number of isomers of pentane (C₅H₁₂) is:", 
     ["2", "3", "4", "5"], 1),
    ("The IUPAC name of the compound CH₃-CH(OH)-CH₃ is:", 
     ["Propan-2-ol", "Propan-1-ol", "Butan-2-ol", "2-Methylpropanol"], 0),
    ("The catalyst used in Haber's process for ammonia synthesis is:", 
     ["Fe", "Ni", "Pt", "V₂O₅"], 0),
    ("The element with atomic number 19 is:", 
     ["Potassium", "Calcium", "Argon", "Scandium"], 0),
    ("The process of heating ore in the absence of air is called:", 
     ["Roasting", "Calcination", "Smelting", "Liquation"], 1),
    ("Which of the following is a noble gas?", 
     ["Nitrogen", "Oxygen", "Argon", "Chlorine"], 2),
    ("The chemical formula of plaster of Paris is:", 
     ["CaSO₄·2H₂O", "CaSO₄·½H₂O", "CaSO₄", "CaCO₃"], 1),
    ("The number of water molecules in gypsum is:", 
     ["1", "2", "0.5", "5"], 1),
    ("The monomer of Teflon is:", 
     ["Ethylene", "Propylene", "Tetrafluoroethylene", "Vinyl chloride"], 2),
    ("The acid present in vinegar is:", 
     ["Acetic acid", "Formic acid", "Citric acid", "Lactic acid"], 0),
    ("The metal that forms an amalgam with other metals is:", 
     ["Mercury", "Lead", "Tin", "Zinc"], 0),
    ("The number of electrons in the valence shell of nitrogen is:", 
     ["2", "5", "7", "8"], 1),
    ("The compound used in anti-malarial drugs is:", 
     ["Chloroquine", "Aspirin", "Paracetamol", "Penicillin"], 0),
    ("The pH of gastric juice is about:", 
     ["1.2", "7.0", "8.5", "10.0"], 0),
    ("Which of the following is not an ore of aluminum?", 
     ["Bauxite", "Cryolite", "Keralaite", "Corundum"], 2),

    # Biology Questions (71-110)
    ("The 'powerhouse of the cell' is:", 
     ["Mitochondria", "Nucleus", "Ribosome", "Golgi apparatus"], 0),
    ("Photosynthesis occurs in which cell organelle?", 
     ["Chloroplast", "Mitochondria", "Nucleus", "Endoplasmic reticulum"], 0),
    ("The basic structural and functional unit of life is:", 
     ["Cell", "Tissue", "Organ", "Organ system"], 0),
    ("Which of the following is not a part of the human digestive system?", 
     ["Stomach", "Liver", "Kidney", "Pancreas"], 2),
    ("The process of cell division in somatic cells is called:", 
     ["Mitosis", "Meiosis", "Binary fission", "Multiple fission"], 0),
    ("The largest gland in the human body is:", 
     ["Liver", "Pancreas", "Pituitary", "Thyroid"], 0),
    ("The blood group which is called universal donor is:", 
     ["A", "B", "AB", "O"], 3),
    ("The process by which plants lose water in the form of vapor is called:", 
     ["Transpiration", "Evaporation", "Condensation", "Precipitation"], 0),
    ("The hormone insulin is secreted by:", 
     ["Pancreas", "Liver", "Kidney", "Thyroid"], 0),
    ("The number of chromosomes in human beings is:", 
     ["23", "46", "48", "50"], 1),
    ("Which of the following is not a nitrogenous base found in DNA?", 
     ["Adenine", "Thymine", "Uracil", "Guanine"], 2),
    ("The site of protein synthesis in a cell is:", 
     ["Ribosome", "Nucleus", "Mitochondria", "Golgi apparatus"], 0),
    ("The process of conversion of light energy to chemical energy occurs in:", 
     ["Photosynthesis", "Respiration", "Transpiration", "Digestion"], 0),
    ("The male reproductive part of a flower is:", 
     ["Stamen", "Pistil", "Petal", "Sepal"], 0),
    ("The study of fossils is called:", 
     ["Paleontology", "Archaeology", "Geology", "Anthropology"], 0),
    ("The longest bone in the human body is:", 
     ["Femur", "Humerus", "Tibia", "Fibula"], 0),
    ("The vitamin which is produced in the human body by exposure to sunlight is:", 
     ["Vitamin A", "Vitamin B", "Vitamin C", "Vitamin D"], 3),
    ("The process of breakdown of glucose to release energy is called:", 
     ["Respiration", "Photosynthesis", "Transpiration", "Digestion"], 0),
    ("The functional unit of kidney is:", 
     ["Nephron", "Neuron", "Alveoli", "Villi"], 0),
    ("Which of the following is not a part of the human respiratory system?", 
     ["Trachea", "Bronchi", "Alveoli", "Esophagus"], 3),
    ("The process of conversion of ammonia to nitrates is called:", 
     ["Nitrogen fixation", "Nitrification", "Denitrification", "Ammonification"], 1),
    ("The hormone that regulates blood sugar level is:", 
     ["Insulin", "Adrenaline", "Thyroxine", "Testosterone"], 0),
    ("The part of the brain that controls balance and coordination is:", 
     ["Cerebellum", "Cerebrum", "Medulla oblongata", "Hypothalamus"], 0),
    ("The process of cell division that produces gametes is called:", 
     ["Meiosis", "Mitosis", "Binary fission", "Budding"], 0),
    ("The smallest bone in the human body is:", 
     ["Stapes", "Femur", "Malleus", "Incus"], 0),
    ("The vitamin responsible for blood clotting is:", 
     ["Vitamin A", "Vitamin B", "Vitamin C", "Vitamin K"], 3),
    ("The process of uptake of water and minerals by roots is called:", 
     ["Absorption", "Adsorption", "Osmosis", "Diffusion"], 0),
    ("The number of chambers in the human heart is:", 
     ["2", "3", "4", "5"], 2),
    ("The pigment responsible for photosynthesis in plants is:", 
     ["Chlorophyll", "Carotene", "Xanthophyll", "Phycobilin"], 0),
    ("The process of conversion of milk to curd is due to:", 
     ["Bacteria", "Virus", "Fungus", "Protozoa"], 0),
    ("The part of the eye that controls the amount of light entering is:", 
     ["Iris", "Pupil", "Cornea", "Retina"], 0),
    ("The disease caused by deficiency of vitamin C is:", 
     ["Scurvy", "Rickets", "Beri-beri", "Night blindness"], 0),
    ("The process of formation of urine is called:", 
     ["Ultrafiltration", "Dialysis", "Secretion", "Excretion"], 0),
    ("The hormone that regulates the sleep-wake cycle is:", 
     ["Melatonin", "Insulin", "Adrenaline", "Thyroxine"], 0),
    ("The part of the plant that conducts water and minerals is:", 
     ["Xylem", "Phloem", "Cambium", "Epidermis"], 0),
    ("The process of transfer of pollen from anther to stigma is called:", 
     ["Pollination", "Fertilization", "Germination", "Reproduction"], 0),
    ("The vitamin which is fat-soluble is:", 
     ["Vitamin A", "Vitamin B", "Vitamin C", "All of these"], 0),
    ("The process of breakdown of food in the presence of oxygen is called:", 
     ["Aerobic respiration", "Anaerobic respiration", "Fermentation", "Glycolysis"], 0),
    ("The part of the cell that contains genetic material is:", 
     ["Nucleus", "Cytoplasm", "Cell membrane", "Ribosome"], 0),
    ("The disease caused by the deficiency of iodine is:", 
     ["Goiter", "Diabetes", "Anemia", "Scurvy"], 0)
]

MOTIVATION_LIST = [
    "💪 Your NEET journey begins with a single chapter. Turn the page.",
    "🔥 Every small effort adds up to success.",
    "⚡ Hard work beats talent when talent doesn't work hard.",
    "🧠 Your future white coat is waiting. Earn it, one chapter at a time.",
    "🌟 The pain of discipline is less than the pain of regret.",
    "📚 Be the doctor you once looked up to.",
    "🎯 Dream it. Believe it. Study for it.",
    "🏔️ The mountain of syllabus is climbed one topic at a time.",
    "🚀 Stuck on a concept? Good. That's where growth happens.",
    "🔬 You are not just reading biology; you're learning the language of life.",
    "⚛️ Every complex reaction has a mechanism. So does your success.",
    "📖 One page, one problem, one hour at a time.",
    "💡 The more you sweat in practice, the less you bleed in the exam.",
    "🎓 You are not just memorizing; you're building a foundation for life.",
    "💫 You are stronger than your strongest excuse.",
    "✨ It's okay to be a glowstick: sometimes you have to break before you shine.",
    "🌈 Don't let a few bad chapters define your entire story.",
    "🌊 You didn't come this far to only come this far.",
    "⏳ Consistency transforms average into exceptional.",
    "🚫 While others are scrolling, you are scoring.",
    "❤️ Your daily routine is a secret love letter to your future self.",
    "🎪 NEET is not just an exam; it's a test of your character.",
    "🔄 Fall seven times, stand up eight for that AIIMS seat.",
    "🎮 Treat each chapter like a level you need to conquer.",
    "🕰️ This year will pass anyway. Make sure you pass with a rank.",
    "💥 Your struggle today is your patient's hope tomorrow.",
    "🎖️ Every topper was once a beginner who never gave up.",
    "🧩 You are solving the puzzle of your future, one subject at a time.",
    "🌱 Growth happens outside your comfort zone. Stay there.",
    "🎵 The rhythm of your pen writing notes is the music of success.",
    "💼 You're not studying; you're building your future clinic.",
    "🦉 Late night studies today for bright white coat tomorrow.",
    "🏆 Your MBBS seat has your name on it. Go claim it.",
    "📈 Progress, not perfection. Every mark counts.",
    "🎨 You are the artist of your NEET success story.",
    "⚓ Your dream college is waiting. Don't keep it waiting.",
    "🌅 Early morning studies separate the ordinary from extraordinary.",
    "💎 Pressure creates diamonds. And future doctors.",
    "🛠️ Your tools: NCERT, determination, and unwavering focus.",
    "🎪 The NEET circus has three rings: Bio, Chem, Physics. Master them all.",
    "🚦 Red light for distractions, green light for studies.",
    "🧭 Lost in syllabus? Your goal is the North Star. Follow it.",
    "💌 Every correct answer is a love letter to your future patients.",
    "🎯 Your focus is your superpower. Don't lose it.",
    "🏃‍♂️ NEET is a marathon. Pace yourself but never stop.",
    "🔄 Revision is the mother of retention. Embrace her.",
    "🌉 You're building a bridge to your dreams. Every study session counts.",
    "🎪 Juggling subjects? That's what future doctors do.",
    "💡 Light will dawn after this darkness. Keep studying.",
    "🦸‍♂️ You are the hero of your NEET story. Act like one.",
    "📊 Mock tests are rehearsals for your grand performance.",
    "🎭 Struggle is temporary. MBBS is permanent.",
    "🧨 Blast through your limits. You're stronger than you think.",
    "🎰 Don't gamble with your future. Study with certainty.",
    "🏹 Your aim is AIIMS. Don't settle for less.",
    "🌙 Stars shine brightest in darkness. So will you.",
    "⚖️ Balance today's fun for tomorrow's success.",
    "🔔 Alarm rings? Time to make your dreams ring true.",
    "🎪 Your mind is the circus. Train every performer: Bio, Chem, Physics.",
    "💪 Muscles grow with stress. So does your brain.",
    "🛌 Tired? Good. That means you're one step closer.",
    "📝 Your pen is mightier than any sword. Wield it wisely.",
    "🎮 Each topic cleared is a level up in the game of NEET.",
    "🌪️ In the storm of syllabus, be the calm, focused eye.",
    "🦅 Eagles fly alone. So do NEET toppers.",
    "💼 Pack your bags with knowledge, not regrets.",
    "🎵 The symphony of your success is composed note by note.",
    "🏆 Victory in NEET is earned in silent, lonely hours.",
    "🔍 Focus on your paper, not others' progress.",
    "🌱 Mighty oaks from little acorns grow. Start small, think big.",
    "⚡ Electricity flows through circuits. Let knowledge flow through you.",
    "🎪 Three subjects, one goal: Doctor.",
    "💎 Your potential is diamond. Pressure will reveal it.",
    "🛣️ The road to MBBS is under construction. You're the engineer.",
    "🎯 Target set: Medical College. Load: Knowledge. Fire!",
    "🧭 Your compass points to success. Don't lose direction.",
    "🌄 Sunrise witnesses your struggle. Sunset will see your success.",
    "📚 Books are your best friends. Make them your allies.",
    "💻 Social media can wait. Your future can't.",
    "🎪 Life's circus will continue. But NEET comes once.",
    "🔄 Yesterday's failure is today's lesson. Learn and move on.",
    "🏹 Arrows hit targets when pulled back. You're being pulled back to launch forward.",
    "💡 Ideas become reality through hard work. Your dream is an idea. Work hard.",
    "🎮 Game Over? Not until you say so. Press Continue.",
    "🌧️ After every storm comes calm. After NEET, comes MBBS.",
    "⚓ Anchor yourself in determination, not distraction.",
    "🎵 Your study playlist: Silence, Focus, Victory.",
    "🏔️ Everest wasn't climbed in a day. Neither will NEET.",
    "🔋 Low battery? Recharge with purpose, not procrastination.",
    "🎪 Center stage: Your study table. Main act: You.",
    "💼 Suit up for success. Your lab coat awaits.",
    "🦉 Wisdom comes from consistent effort, not occasional studying.",
    "🚀 Launch sequence initiated: T-minus 365 days to NEET.",
    "🎯 Bullseye: Your dream college. Your arrow: Preparation.",
    "🌱 Plant seeds of knowledge today. Harvest success tomorrow.",
    "⚖️ Weigh your priorities: Temporary fun vs Permanent career.",
    "🔔 Your conscience is the best alarm clock. Listen to it.",
    "🎪 Life's big top has your name. But first, NEET.",
    "💪 Strong minds overcome weak moments. Be strong.",
    "📈 Your growth graph: Upwards and onwards. Always.",
    "🎮 You're not playing games; you're building your future.",
    "🌪️ In the tornado of competition, be the calm strategist.",
    "🦅 Soar above doubts. Your sky is limitless.",
    "💼 Your briefcase: Confidence, Knowledge, Determination.",
    "🎵 The music of success is played on strings of hard work.",
    "🏆 Champions are made when no one is watching. Study now.",
    "🔍 Zoom in on goals, blur out distractions.",
    "🌱 Great oaks from little NCERTs grow.",
    "⚡ Be the current that powers through obstacles.",
    "🎪 Three rings, one dream: White Coat.",
    "💎 Your value increases with every challenge faced.",
    "🛣️ The path is tough. So are you. Keep walking.",
    "🎯 Your target is clear. Your vision should be too."
]

DAILY_CHALLENGE_LIST = [
    # Physics (35 Questions)
    "🧠 Physics: A charged particle moving in a magnetic field experiences a force. Why?",
    "🧠 Physics: What is the principle behind an electric generator?",
    "🧠 Physics: Derive the equation for time period of a simple pendulum.",
    "🧠 Physics: Explain Newton's laws of motion with examples.",
    "🧠 Physics: What is conservation of angular momentum?",
    "🧠 Physics: Define work-energy theorem.",
    "🧠 Physics: What is the difference between elastic and inelastic collisions?",
    "🧠 Physics: Explain Kirchhoff's laws of electrical circuits.",
    "🧠 Physics: What is Snell's law of refraction?",
    "🧠 Physics: Define capacitance of a parallel plate capacitor.",
    "🧠 Physics: Explain photoelectric effect and its significance.",
    "🧠 Physics: What is Bohr's model of hydrogen atom?",
    "🧠 Physics: Define simple harmonic motion with examples.",
    "🧠 Physics: What are the laws of thermodynamics?",
    "🧠 Physics: Explain wave-particle duality.",
    "🧠 Physics: What is the difference between AC and DC?",
    "🧠 Physics: Define electric dipole moment.",
    "🧠 Physics: What is Gauss's law in electrostatics?",
    "🧠 Physics: Explain the working of a transformer.",
    "🧠 Physics: What is the concept of escape velocity?",
    "🧠 Physics: Define magnetic susceptibility.",
    "🧠 Physics: What is the principle of superposition of waves?",
    "🧠 Physics: Explain Huygens principle.",
    "🧠 Physics: What is the difference between isothermal and adiabatic processes?",
    "🧠 Physics: Define Young's modulus of elasticity.",
    "🧠 Physics: What are the applications of Bernoulli's principle?",
    "🧠 Physics: Explain the concept of interference of light.",
    "🧠 Physics: What is the Heisenberg uncertainty principle?",
    "🧠 Physics: Define decay constant in radioactivity.",
    "🧠 Physics: What is the working principle of a p-n junction diode?",
    "🧠 Physics: Explain the formation of rainbow.",
    "🧠 Physics: What is the difference between nuclear fission and fusion?",
    "🧠 Physics: Define coefficient of performance of a refrigerator.",
    "🧠 Physics: What is the significance of Maxwell's equations?",
    "🧠 Physics: Explain the concept of equipotential surfaces.",

    # Chemistry (35 Questions)
    "⚡ Chemistry: Explain hybridisation in methane molecule.",
    "⚡ Chemistry: What is the difference between ionic and covalent bonds?",
    "⚡ Chemistry: Define Le Chatelier's principle.",
    "⚡ Chemistry: What are the postulates of kinetic theory of gases?",
    "⚡ Chemistry: Explain the order of reactivity in haloalkanes.",
    "⚡ Chemistry: What is the IUPAC name of CH3-CH2-COOH?",
    "⚡ Chemistry: Define the laws of chemical combination.",
    "⚡ Chemistry: What is the structure of benzene?",
    "⚡ Chemistry: Explain the preparation and properties of alkanes.",
    "⚡ Chemistry: What are the differences between alcohols and phenols?",
    "⚡ Chemistry: Define mole concept with examples.",
    "⚡ Chemistry: What is the VSEPR theory?",
    "⚡ Chemistry: Explain the classification of elements in periodic table.",
    "⚡ Chemistry: What are coordination compounds?",
    "⚡ Chemistry: Define the terms: oxidation and reduction.",
    "⚡ Chemistry: What is the Henderson-Hasselbalch equation?",
    "⚡ Chemistry: Explain the collision theory of reaction rates.",
    "⚡ Chemistry: What are the different types of solutions?",
    "⚡ Chemistry: Define the terms: isotonic, hypotonic and hypertonic solutions.",
    "⚡ Chemistry: What is the difference between roasting and calcination?",
    "⚡ Chemistry: Explain the extraction of aluminium from bauxite.",
    "⚡ Chemistry: What are the uses of sodium carbonate?",
    "⚡ Chemistry: Define the terms: enantiomers and diastereomers.",
    "⚡ Chemistry: What is the E1 and E2 elimination mechanism?",
    "⚡ Chemistry: Explain the preparation of potassium permanganate.",
    "⚡ Chemistry: What are the different types of polymers?",
    "⚡ Chemistry: Define the terms: adsorption and absorption.",
    "⚡ Chemistry: What is the difference between nucleophilic and electrophilic substitution?",
    "⚡ Chemistry: Explain the Werner's theory of coordination compounds.",
    "⚡ Chemistry: What are the uses of hydrogen peroxide?",
    "⚡ Chemistry: Define the terms: molality and molarity.",
    "⚡ Chemistry: What is the structure and bonding in B2H6?",
    "⚡ Chemistry: Explain the preparation of ethers from alcohols.",
    "⚡ Chemistry: What are the characteristics of transition elements?",
    "⚡ Chemistry: Define the terms: crystal field splitting and crystal field stabilization energy.",

    # Biology (35 Questions)
    "💉 Biology: Why mitochondria are called powerhouses of the cell?",
    "💉 Biology: What is the difference between mitosis and meiosis?",
    "💉 Biology: Explain the process of DNA replication.",
    "💉 Biology: What are the different types of plant tissues?",
    "💉 Biology: Define the structure and function of nephron.",
    "💉 Biology: What is the sliding filament theory of muscle contraction?",
    "💉 Biology: Explain the menstrual cycle in human females.",
    "💉 Biology: What are the functions of liver in human body?",
    "💉 Biology: Define the terms: genotype and phenotype.",
    "💉 Biology: What is the difference between innate and acquired immunity?",
    "💉 Biology: Explain the process of photosynthesis.",
    "💉 Biology: What are the different types of ecological pyramids?",
    "💉 Biology: Define the structure of human heart.",
    "💉 Biology: What is the Hardy-Weinberg principle?",
    "💉 Biology: Explain the nitrogen cycle in nature.",
    "💉 Biology: What are the functions of plant growth regulators?",
    "💉 Biology: Define the terms: dominant and recessive traits.",
    "💉 Biology: What is the difference between prokaryotic and eukaryotic cells?",
    "💉 Biology: Explain the process of protein synthesis.",
    "💉 Biology: What are the different types of chromosomes?",
    "💉 Biology: Define the structure and function of neuron.",
    "💉 Biology: What is the double circulation in human heart?",
    "💉 Biology: Explain the process of fertilization in flowering plants.",
    "💉 Biology: What are the functions of different parts of brain?",
    "💉 Biology: Define the terms: homologous and analogous organs.",
    "💉 Biology: What is the difference between C3 and C4 plants?",
    "💉 Biology: Explain the process of respiration in humans.",
    "💉 Biology: What are the different types of plant movements?",
    "💉 Biology: Define the structure and function of chloroplast.",
    "💉 Biology: What is the process of urine formation?",
    "💉 Biology: Explain the theory of natural selection.",
    "💉 Biology: What are the different types of animal tissues?",
    "💉 Biology: Define the terms: parasitism and mutualism.",
    "💉 Biology: What is the difference between blood and lymph?",
    "💉 Biology: Explain the process of digestion in human alimentary canal.",

    # Bonus Questions (5 Questions)
    "🧠 Physics: What is the difference between mass and weight?",
    "⚡ Chemistry: What is the pH of a neutral solution at 25°C?",
    "💉 Biology: What is the full form of DNA?",
    "🧠 Physics: State the law of conservation of energy.",
    "⚡ Chemistry: What is the electronic configuration of carbon?"
]
# ---------------- HELPERS ----------------
def build_main_menu():
    keyboard = [
        [
            InlineKeyboardButton("📚 Access Courses", url=COURSE_LINK),
            InlineKeyboardButton("💬 Ask Admin", url=f"https://t.me/{ADMIN_USERNAME}")
        ],
        [
            InlineKeyboardButton("🎯 Random Quiz", callback_data="menu_quiz"),
            InlineKeyboardButton("💡 Daily Motivation", callback_data="menu_tips")
        ],
        [
            InlineKeyboardButton("🧠 Daily Challenge", callback_data="menu_challenge")
        ],
        [
            InlineKeyboardButton("🛒 How to Buy", url=HOW_TO_BUY_LINK)
        ]
    ]
    return InlineKeyboardMarkup(keyboard)

def get_random_quiz_index(user_id):
    """Get a random quiz index that user hasn't answered recently"""
    if user_id not in user_answered_questions:
        user_answered_questions[user_id] = set()
    
    available_indices = set(range(len(QUIZ_LIST))) - user_answered_questions[user_id]
    
    if not available_indices:
        # Reset if all questions have been answered
        user_answered_questions[user_id] = set()
        available_indices = set(range(len(QUIZ_LIST)))
    
    return random.choice(list(available_indices))

def build_quiz_keyboard(q_index):
    q_text, choices, _ = QUIZ_LIST[q_index]
    keyboard = []
    for i, choice in enumerate(choices):
        callback = f"quiz|{q_index}|{i}"
        keyboard.append([InlineKeyboardButton(f"{chr(65+i)}) {choice}", callback_data=callback)])
    keyboard.append([
        InlineKeyboardButton("⏭️ Skip", callback_data="quiz_skip"),
        InlineKeyboardButton("🏠 Main Menu", callback_data="menu_main")
    ])
    return InlineKeyboardMarkup(keyboard)

# ---------------- HANDLERS ----------------
def start(update: Update, context: CallbackContext):
    name = update.effective_user.first_name or "Aspirant"
    msg = (
        f"🚀 <b>Hey {html.escape(name)}, ready to conquer NEET?</b> 🚀\n\n"
        "Welcome to <b>NainoAcademy</b> — your ultimate companion for NEET preparation!\n\n"
        "<b>Pick an option below and let's get started:</b>"
    )
    update.message.reply_text(msg, parse_mode=ParseMode.HTML, reply_markup=build_main_menu())

def callback_router(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()
    data = query.data
    user_id = query.from_user.id

    if data == "menu_main":
        query.edit_message_text("🏠 <b>Back to Main Menu:</b>", reply_markup=build_main_menu(), parse_mode=ParseMode.HTML)
        return

    if data == "menu_tips":
        tip = random.choice(MOTIVATION_LIST)
        query.edit_message_text(f"💡 <b>Daily Motivation:</b>\n\n{tip}", 
                               parse_mode=ParseMode.HTML, 
                               reply_markup=build_main_menu())
        return

    if data == "menu_challenge":
        now = time.time()
        last_time = user_cooldowns.get(user_id, {}).get('challenge', 0)
        
        if now - last_time < 60:  # 60 seconds cooldown
            remaining = int(60 - (now - last_time))
            query.edit_message_text(
                f"⏳ <b>Challenge Cooldown!</b>\n\n"
                f"Try again in <b>{remaining}</b> seconds! 🔄",
                parse_mode=ParseMode.HTML,
                reply_markup=build_main_menu()
            )
            return
        
        # Update cooldown
        if user_id not in user_cooldowns:
            user_cooldowns[user_id] = {}
        user_cooldowns[user_id]['challenge'] = now
        
        challenge = random.choice(DAILY_CHALLENGE_LIST)
        query.edit_message_text(f"🧠 <b>Today's Challenge:</b>\n\n{challenge}\n\n<i>Next challenge available in 60 seconds ⏰</i>",
                                parse_mode=ParseMode.HTML,
                                reply_markup=build_main_menu())
        return

    if data == "menu_quiz":
        q_index = get_random_quiz_index(user_id)
        user_answered_questions[user_id].add(q_index)
        
        q_text, choices, _ = QUIZ_LIST[q_index]
        
        # Create animated loading message
        loading_msg = query.edit_message_text(
            "🎯 <b>Loading Random Quiz...</b> ⏳",
            parse_mode=ParseMode.HTML
        )
        
        # Simulate loading (small delay for better UX)
        time.sleep(0.5)
        
        query.edit_message_text(f"🎯 <b>Quiz Time!</b>\n\n{html.escape(q_text)}",
                                parse_mode=ParseMode.HTML,
                                reply_markup=build_quiz_keyboard(q_index))
        return

    if data.startswith("quiz|"):
        parts = data.split("|")
        q_index, choice_index = int(parts[1]), int(parts[2])
        correct = QUIZ_LIST[q_index][2]
        if user_id not in user_scores:
            user_scores[user_id] = 0

        # Add small delay for better UX
        time.sleep(0.3)
        
        if choice_index == correct:
            user_scores[user_id] += 1
            reply = f"🎉 <b>Correct!</b> ✅\n\nTotal Score: <b>{user_scores[user_id]}</b> points 🏆"
        else:
            correct_letter = chr(65 + correct)
            ans = QUIZ_LIST[q_index][1][correct]
            reply = f"❌ <b>Incorrect!</b>\n\nCorrect Answer: <b>{correct_letter}) {ans}</b>\n\nTotal Score: <b>{user_scores[user_id]}</b> points 🎯"

        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("🔥 Next Random Quiz", callback_data="menu_quiz"),
             InlineKeyboardButton("🏠 Main Menu", callback_data="menu_main")]
        ])
        query.edit_message_text(reply, parse_mode=ParseMode.HTML, reply_markup=keyboard)
        return

    if data == "quiz_skip":
        query.edit_message_text("⏭️ <b>Question skipped!</b>\n\nReady for the next challenge? 🔥",
                                reply_markup=InlineKeyboardMarkup([
                                    [InlineKeyboardButton("🔥 Next Random Quiz", callback_data="menu_quiz"),
                                     InlineKeyboardButton("🏠 Main Menu", callback_data="menu_main")]
                                ]),
                                parse_mode=ParseMode.HTML)
        return

def main():
    if BOT_TOKEN.startswith("YOUR_"):
        print("❌ Add your Telegram bot token first.")
        return
    
    # Create updater with optimized settings
    updater = Updater(
        BOT_TOKEN, 
        use_context=True,
        request_kwargs={'read_timeout': 10, 'connect_timeout': 10}
    )
    
    dp = updater.dispatcher
    
    # Add error handler for better stability
    def error_handler(update: Update, context: CallbackContext):
        print(f"Error occurred: {context.error}")
    
    dp.add_error_handler(error_handler)
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CallbackQueryHandler(callback_router))
    
    print("🚀 Bot running with enhanced performance...")
    print("📊 Features:")
    print("   ✅ Random quiz selection")
    print("   ✅ 60-second challenge cooldown") 
    print("   ✅ Improved UI with animations")
    print("   ✅ Better performance")
    print("   ✅ Enhanced user experience")
    
    updater.start_polling(
        poll_interval=0.5,  # Faster polling
        timeout=20,
        drop_pending_updates=True  # Clean start
    )
    updater.idle()

if __name__ == "__main__":
    main()