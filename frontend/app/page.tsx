import { redirect } from 'next/navigation'

export default function HomePage() {
  // Redirect to dashboard for authenticated users
  // This will be handled by middleware, but we provide a fallback
  redirect('/dashboard')
}