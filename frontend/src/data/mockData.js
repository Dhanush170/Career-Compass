// src/data/mockData.js

export const mockData = {
  // --- FROM YOUR PYTHON OUTPUT ---
  ats_score: 42.0,
  ats_band: 'Weak Match',
  suggestion: 'Current resume has a low match. You can significantly improve your match by adding skills like: linux, perl, shell. Improve formatting by using clear sections.',
  
  missing_skills: [
    'linux', 'perl', 'shell', 'technical skills', 'understanding linux'
  ],

  scores: {
    keyword_score: 28.3,
    semantic_score: 45.4,
    format_score: 60.0,
    experience_score: 50.0
  },

  meta: {
    resume_word_count: 214,
    jd_word_count: 308,
    skill_level_count: 19,
    booster_count: 2,
    learning_steps: 5
  },

  // --- FROM YOUR COMPACT JSON PAYLOAD ---
  primary_role: "Software Engineer",
  
  roles: [
    {
      role: "Software Engineer",
      score: 0.90,
      matched_skills: ["Python", "C++", "Java", "HTML", "CSS", "SQL", "Git"],
      evidence: "Programming Languages: C++, Python, Java...",
      reason: "Strong foundational programming skills in Python, C++, and Java applied to build functional web apps."
    },
    {
      role: "Technical Consultant",
      score: 0.85,
      matched_skills: ["Python", "HTML", "CSS", "Streamlit", "Flask"],
      evidence: "Specializing in CS and Business Systems, passion for digital solutions...",
      reason: "Passion for user-centric solutions aligns with technical consultant role."
    },
    {
      role: "Backend Developer",
      score: 0.80,
      matched_skills: ["Python", "Flask", "Streamlit", "LangChain", "SQL"],
      evidence: "RPSAT is a Streamlit web app... Crop Recommendation System...",
      reason: "Strong backend capabilities utilizing Python with frameworks like Flask/Streamlit."
    }
  ],

  skill_levels: [
    { name: "Python", level: "Intermediate", confidence: 90 },
    { name: "Streamlit", level: "Intermediate", confidence: 90 },
    { name: "Flask", level: "Intermediate", confidence: 90 },
    { name: "LangChain", level: "Intermediate", confidence: 90 },
    { name: "HTML/CSS", level: "Intermediate", confidence: 80 },
    { name: "C++", level: "Beginner", confidence: 60 },
    { name: "Java", level: "Beginner", confidence: 60 },
    { name: "SQL", level: "Beginner", confidence: 60 }
  ],

  booster_suggestions: [
    {
      skill: "aws",
      snippet: "Deployed and managed scalable web applications on AWS EC2 instances, leveraging S3 for storage.",
      derived_from_resume: false,
      confidence: 0
    },
    {
      skill: "linux",
      snippet: "Utilized Linux environments for development and deployment, managing system configurations and shell scripting tasks.",
      derived_from_resume: false,
      confidence: 0
    }
  ],

  learning_path: [
    { step: 1, title: "Linux Command Line Fundamentals", type: "course", duration_weeks: 3.0, notes: "Build a strong foundation in Linux, covering essential commands and shell scripting." },
    { step: 2, title: "Practical Linux SysAdmin", type: "practice", duration_weeks: 2.0, notes: "Apply learned Linux commands through hands-on exercises." },
    { step: 3, title: "AWS Cloud Practitioner Essentials", type: "course", duration_weeks: 4.0, notes: "Gain an overview of AWS core services like EC2, S3, and VPC." },
    { step: 4, title: "Deploying Python App on EC2", type: "project", duration_weeks: 3.0, notes: "Deploy your Flask/Streamlit projects onto an AWS EC2 instance." }
  ],

  future_trends: [
    { name: "Cloud Computing", why: "Foundational for deploying scalable applications." },
    { name: "Containerization (Docker)", why: "Crucial for building portable microservices." },
    { name: "LLM Deployment & MLOps", why: "High-demand specialization for RAG pipelines." }
  ]
};