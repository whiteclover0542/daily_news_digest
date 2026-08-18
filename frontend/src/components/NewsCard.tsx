import { Link } from 'react-router-dom'
import type { NewsListItem } from '../api/types'

export default function NewsCard({ item }: { item: NewsListItem }) {
  return (
    <Link to={`/news/${item.id}`} className="news-card">
      <span className="news-card__category">{item.category.name}</span>
      <h2 className="news-card__title">{item.title}</h2>
      <p className="news-card__summary">{item.summary_preview}</p>
      <span className="news-card__source">{item.source}</span>
    </Link>
  )
}
