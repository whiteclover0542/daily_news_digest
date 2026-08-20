import { useEffect, useState } from 'react'
import CategoryTabs from '../components/CategoryTabs'
import NewsCard from '../components/NewsCard'
import { fetchCategories, fetchNews } from '../api/client'
import type { Category, NewsListItem } from '../api/types'

export default function MainPage() {
  const [categories, setCategories] = useState<Category[]>([])
  const [selectedSlug, setSelectedSlug] = useState<string | null>(null)
  const [items, setItems] = useState<NewsListItem[]>([])
  const [date, setDate] = useState('')
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    fetchCategories()
      .then(setCategories)
      .catch(() => {
        /* 카테고리 탭은 못 불러와도 목록 조회는 계속 진행 */
      })
  }, [])

  useEffect(() => {
    setLoading(true)
    setError(null)
    fetchNews({ category: selectedSlug ?? undefined })
      .then((res) => {
        setItems(res.items)
        setDate(res.date)
      })
      .catch(() => setError('뉴스를 불러오지 못했습니다.'))
      .finally(() => setLoading(false))
  }, [selectedSlug])

  return (
    <main className="page">
      <header className="page-header">
        <h1>오늘의 뉴스</h1>
        {date && <p>{date}</p>}
      </header>

      <CategoryTabs categories={categories} selected={selectedSlug} onSelect={setSelectedSlug} />

      {loading && <p className="state-message">불러오는 중...</p>}
      {!loading && error && <p className="state-message error">{error}</p>}
      {!loading && !error && items.length === 0 && (
        <p className="state-message">오늘 등록된 뉴스가 없습니다.</p>
      )}

      <div className="news-list">
        {items.map((item) => (
          <NewsCard key={item.id} item={item} />
        ))}
      </div>
    </main>
  )
}
