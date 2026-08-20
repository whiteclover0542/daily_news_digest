import { useEffect, useState } from 'react'
import { Link, useParams } from 'react-router-dom'
import { fetchNewsDetail } from '../api/client'
import type { NewsDetail } from '../api/types'

export default function DetailPage() {
  const { id } = useParams<{ id: string }>()
  const [detail, setDetail] = useState<NewsDetail | null>(null)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    if (!id) return
    setError(null)
    setDetail(null)
    fetchNewsDetail(Number(id))
      .then(setDetail)
      .catch(() => setError('기사를 불러오지 못했습니다.'))
  }, [id])

  return (
    <main className="page">
      <Link to="/" className="back-link">
        ← 목록으로
      </Link>

      {error && <p className="state-message error">{error}</p>}
      {!error && !detail && <p className="state-message">불러오는 중...</p>}

      {detail && (
        <article className="detail-page">
          <span className="detail-page__category">{detail.category.name}</span>
          <h1>{detail.title}</h1>
          <p className="detail-page__meta">
            {detail.source} · {new Date(detail.published_at).toLocaleString('ko-KR')}
          </p>
          <p className="detail-page__summary">{detail.summary}</p>
          {detail.keywords.length > 0 && (
            <div className="detail-page__keywords">
              {detail.keywords.map((keyword) => (
                <span key={keyword} className="keyword-chip">
                  #{keyword}
                </span>
              ))}
            </div>
          )}
          <a href={detail.url} target="_blank" rel="noreferrer" className="detail-page__link">
            원문 보기
          </a>
        </article>
      )}
    </main>
  )
}
