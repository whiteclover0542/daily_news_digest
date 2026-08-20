export interface Category {
  id: number
  name: string
  slug: string
}

export interface NewsListItem {
  id: number
  title: string
  source: string
  category: Category
  summary_preview: string
  published_at: string
}

export interface NewsListResponse {
  date: string
  total: number
  page: number
  limit: number
  items: NewsListItem[]
}

export interface NewsDetail {
  id: number
  title: string
  source: string
  url: string
  category: Category
  summary: string
  keywords: string[]
  published_at: string
  collected_at: string
}
