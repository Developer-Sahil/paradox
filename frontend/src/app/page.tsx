import GlassCard from '@/components/GlassCard';
import { api, Post } from '@/lib/api';

async function getLatestPosts(): Promise<Post[]> {
  try {
    const posts = await api.getWritings();
    return posts.slice(0, 3); // Get latest 3 posts
  } catch (error) {
    console.error('Failed to fetch posts:', error);
    return [];
  }
}

export default async function Home() {
  const latestPosts = await getLatestPosts();

  return (
    <main className="flex flex-grow flex-col items-center justify-center py-16 px-8 sm:px-16 lg:px-24">
      <GlassCard className="p-8 sm:p-12 lg:p-16 max-w-4xl w-full mx-auto my-8">
        <h1 className="text-5xl font-extrabold text-accent-light drop-shadow-lg text-center leading-tight">
          Welcome Home!
        </h1>
        <p className="mt-6 text-xl text-text-secondary text-center max-w-prose mx-auto">
          This is a beautifully designed glassmorphic card on your home page, demonstrating intentional spacing and a premium feel.
        </p>
      </GlassCard>

      {/* Latest Writings */}
      {latestPosts.length > 0 && (
        <section className="w-full max-w-6xl mt-12">
          <h2 className="text-3xl font-bold text-accent-light mb-6">Latest Writings</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {latestPosts.map((post) => (
              <GlassCard key={post.id} className="p-6 hover:scale-105 transition-transform">
                <time className="text-sm text-text-secondary">{post.date}</time>
                <h3 className="text-xl font-semibold text-accent-light mt-2 mb-3">
                  {post.title}
                </h3>
                <p className="text-text-secondary line-clamp-3">
                  {post.content.substring(0, 150)}...
                </p>
                {post.tags.length > 0 && (
                  <div className="flex flex-wrap gap-2 mt-4">
                    {post.tags.map((tag) => (
                      <span
                        key={tag}
                        className="px-3 py-1 bg-accent-DEFAULT bg-opacity-20 rounded-full text-xs text-accent-light"
                      >
                        {tag}
                      </span>
                    ))}
                  </div>
                )}
              </GlassCard>
            ))}
          </div>
        </section>
      )}
    </main>
  );
}