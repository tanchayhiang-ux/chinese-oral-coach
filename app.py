import streamlit as st
import random
import speech_recognition as sr
from PIL import Image

st.set_page_config(
    page_title="华文口试练习助手",
    page_icon="🎤",
    layout="wide"
)

# =====================
# QUESTION BANK
# =====================

questions = [
    {
        "question": "你和家人去动物园，看见有人乱丢垃圾。你会怎么做？",
        "keywords": ["劝告", "垃圾", "环保", "清洁"],
        "image": "https://images.unsplash.com/photo-1549366021-9f761d450615?w=800"
    },
    {
        "question": "你在食堂排队买食物时，有同学插队。你会怎么处理？",
        "keywords": ["礼貌", "排队", "规则"],
        "image": "https://images.unsplash.com/photo-1504674900247-0877df9cc836?w=800"
    },
    {
        "question": "学校举办义卖会，你会怎样帮助老师？",
        "keywords": ["帮助", "责任", "合作"],
        "image": "https://images.unsplash.com/photo-1517486808906-6ca8b3f04846?w=800"
    },
    {
        "question": "你在公园看到一位老奶奶跌倒了。你会怎么做？",
        "keywords": ["帮助", "关心", "安全"],
        "image": "https://images.unsplash.com/photo-1516589178581-6cd7833ae3b2?w=800"
    },
    {
        "question": "你和朋友发生误会，你会怎样解决？",
        "keywords": ["沟通", "道歉", "理解"],
        "image": "https://images.unsplash.com/photo-1529156069898-49953e39b3ac?w=800"
    }
]

# =====================
# SESSION STATE
# =====================

if "score" not in st.session_state:
    st.session_state.score = 0

if "question" not in st.session_state:
    st.session_state.question = random.choice(questions)

# =====================
# HEADER
# =====================

st.title("🎤 华文口试练习助手")
st.subheader("适合10岁学生的华文会话练习")

st.info(
    f"🏆 当前分数: {st.session_state.score}"
)

# =====================
# SHOW SCENARIO
# =====================

q = st.session_state.question

st.image(q["image"], width=600)

st.markdown("### 情景")
st.write(q["question"])

# =====================
# STUDENT RESPONSE
# =====================

response = st.text_area(
    "请输入你的回答（可先用语音输入）：",
    height=150
)

# =====================
# SIMPLE EVALUATION
# =====================

def evaluate_answer(answer, keywords):

    score = 0

    matched = 0

    for word in keywords:
        if word in answer:
            matched += 1

    score = matched * 2

    length_bonus = min(len(answer) // 15, 4)

    score += length_bonus

    score = min(score, 10)

    if score >= 8:
        feedback = "🌟 很好！你的回答完整，也表达了正确的价值观。"
    elif score >= 5:
        feedback = "👍 不错！可以再多说一些原因和做法。"
    else:
        feedback = "😊 再试试看。记得说明你会怎么做和为什么这样做。"

    return score, feedback

# =====================
# SUBMIT
# =====================

if st.button("提交回答"):

    if response.strip() == "":
        st.warning("请先输入回答。")

    else:

        score, feedback = evaluate_answer(
            response,
            q["keywords"]
        )

        st.session_state.score += score

        st.success(f"本题得分：{score}/10")
        st.write(feedback)

        st.markdown("### 建议")

        if score < 5:
            st.write(
                "尝试使用完整句子，并说明：\n"
                "- 发生了什么事\n"
                "- 你会怎么做\n"
                "- 为什么这样做"
            )

# =====================
# NEXT QUESTION
# =====================

if st.button("下一题"):

    st.session_state.question = random.choice(questions)
    st.rerun()

# =====================
# SCORE BOARD
# =====================

st.markdown("---")
st.subheader("🏅 总分")

st.metric(
    label="累计得分",
    value=st.session_state.score
)

st.markdown("""
### 评分标准

⭐ 0-4分：回答太短

⭐⭐ 5-7分：回答基本完整

⭐⭐⭐ 8-10分：回答详细，有原因和例子
""")
