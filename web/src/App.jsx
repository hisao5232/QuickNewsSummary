import { useState, useEffect } from "react";

function App() {
  const [news, setNews] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch("https://quicknews-api.go-pro-world.net/news?limit=10")
      .then((res) => res.json())
      .then((data) => {
        console.log("APIレスポンス:", data);
        setNews(data);
        setLoading(false);
      })
      .catch((err) => {
        console.error("API取得エラー:", err);
        setLoading(false);
      });
  }, []);

  if (loading) return <div>読み込み中...</div>;

  return (
    <div>
      <h1>Quick News Viewer</h1>
      <p>表示件数: {news.length}</p>
      <ul>
        {news.map((item) => (
          <li key={item.id}>
            <a href={item.href} target="_blank" rel="noopener noreferrer">
              {item.title}
            </a>
            <p>{item.content}</p>
            <small>{item.scraped_at}</small>
          </li>
        ))}
      </ul>
    </div>
  );
}

export default App;
