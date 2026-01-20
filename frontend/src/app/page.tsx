import GlassCard from '@/components/GlassCard';

export default function Home() {
  return (
    <main className="flex flex-grow flex-col items-center justify-center py-16 px-8 sm:px-16 lg:px-24">
      <GlassCard className="p-8 sm:p-12 lg:p-16 max-w-4xl w-full mx-auto my-8">
        <h1 className="text-5xl font-extrabold text-accent-light drop-shadow-lg text-center leading-tight">Welcome Home!</h1>
        <p className="mt-6 text-xl text-text-secondary text-center max-w-prose mx-auto">This is a beautifully designed glassmorphic card on your home page, demonstrating intentional spacing and a premium feel.</p>
      </GlassCard>
    </main>
  );
}
