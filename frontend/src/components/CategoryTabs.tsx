import type { Category } from '../api/types'

interface CategoryTabsProps {
  categories: Category[]
  selected: string | null
  onSelect: (slug: string | null) => void
}

export default function CategoryTabs({ categories, selected, onSelect }: CategoryTabsProps) {
  return (
    <div className="category-tabs">
      <button type="button" className={selected === null ? 'active' : ''} onClick={() => onSelect(null)}>
        전체
      </button>
      {categories.map((category) => (
        <button
          key={category.id}
          type="button"
          className={selected === category.slug ? 'active' : ''}
          onClick={() => onSelect(category.slug)}
        >
          {category.name}
        </button>
      ))}
    </div>
  )
}
