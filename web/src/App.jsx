import { useState, useEffect } from "react";

function App() {
  const [news, setNews] = useState([]);
  const [loading, setLoading] = useState(true);
  const [date, setDate] = useState("");

  useEffect(() => {
    fetch("https://quicknews-api.go-pro-world.net/news?limit=100")
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

  // ✅ ここで filteredNews を定義する
  const filteredNews = date
    ? news.filter((item) => item.scraped_at.startsWith(date))
    : news;

  return (
    <div>
      <h1>Quick News Viewer</h1>
      <input
        type="date"
        value={date}
        onChange={(e) => setDate(e.target.value)}
      />
      {loading ? (
        <p>読み込み中...</p>
      ) : (
        <div>
          <p>表示件数: {filteredNews.length}</p>
          <ul>
            {filteredNews.map((item) => (
              <li key={item.id}>
                <a href={item.href} target="_blank" rel="noopener noreferrer">
                  {item.title}
                </a>
                <br />
                取得日時: {new Date(item.scraped_at).toLocaleString()}
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}

export default App;
