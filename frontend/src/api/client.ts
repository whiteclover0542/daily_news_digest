import type { Category, NewsDetail, NewsListResponse } from './types'

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL ?? 'http://localhost:8000/api'

async function request<T>(path: string): Promise<T> {
  const res = await fetch(`${API_BASE_URL}${path}`)
  if (!res.ok) {
    throw new Error(`API request failed: ${res.status}`)
  }
  return res.json() as Promise<T>
}

export function fetchCategories(): Promise<Category[]> {
  return request<Category[]>('/categories')
}

export function fetchNews(params: { category?: string; page?: number } = {}): Promise<NewsListResponse> {
  const search = new URLSearchParams()
  if (params.category) search.set('category', params.category)
  if (params.page) search.set('page', String(params.page))
  const qs = search.toString()
  return request<NewsListResponse>(`/news${qs ? `?${qs}` : ''}`)
}

export function fetchNewsDetail(id: number): Promise<NewsDetail> {
  return request<NewsDetail>(`/news/${id}`)
}
