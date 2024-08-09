import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.tag import pos_tag
from collections import Counter
from string import punctuation
from redis import Redis
from database.models import DbPost
from sqlalchemy.orm import Session
import json 


nltk.download("punkt")
nltk.download("stopwords")
nltk.download("averaged_perceptron_tagger")

def extract_topic(text: str):
    stop_words = set(stopwords.words("english"))
    words = word_tokenize(text)
    words = [word.lower() for word in words if word.isalnum()]
    words = [word for word in words if word not in stop_words]
    words = [word for word in words if word not in punctuation]
    words = [word for word in words if not word.isdigit()]
    tagged_words = pos_tag(words)
    topics = [word for word, pos in tagged_words if pos.startswith("NN")]
    return topics

def update_trending_topics(db: Session, redis: Redis):
    recent_posts = db.query(DbPost.content, DbPost.title).order_by(DbPost.created_at.desc()).limit(100).all()
    all_topics = []
    if recent_posts:
        for post in recent_posts:
            topics = extract_topic(post[1] + " " + post[0])
            all_topics.extend(topics)
        topic_counts = Counter(all_topics)
        sorted_topic_counts = topic_counts.most_common(10)
        redis.set("trending_topics", json.dumps(sorted_topic_counts))
        redis.expire("trending_topics", 3600*12)
    else:
        return None

def get_trending_topics(db: Session, redis: Redis):
    trending_topics = redis.get("trending_topics")
    if trending_topics:
        return json.loads(trending_topics)
    else:
        update_trending_topics(db)
        return json.loads(redis.get("trending_topics"))

async def scheduled_update_trending_topics():
    pass
