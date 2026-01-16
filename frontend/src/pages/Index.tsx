import { useState } from "react";
import { Container } from "lucide-react";
import SearchBar from "@/components/SearchBar";
import ResultDisplay from "@/components/ResultDisplay";

const Index = () => {
  const [query, setQuery] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [naturalLanguageResult, setNaturalLanguageResult] = useState<string | null>(null);

  const handleSearch = async (searchQuery: string) => {
    setQuery(searchQuery);
    setIsLoading(true);
    setNaturalLanguageResult(null);

    // Simulate API call - will be replaced with actual MongoDB + LLM integration
    setTimeout(() => {
      setNaturalLanguageResult(
        `Based on your query "${searchQuery}", I found 42 matching records in the database. The data shows 3 sample items with values ranging from 95 to 280. The average value across these items is approximately 175. Would you like me to filter or analyze this data further?`
      );
      setIsLoading(false);
    }, 2000);
  };

  return (
    <div className="min-h-screen bg-background grid-bg relative overflow-hidden">
      {/* Ambient glow effects */}
      <div className="absolute top-0 left-1/4 w-96 h-96 bg-primary/5 rounded-full blur-3xl pointer-events-none" />
      <div className="absolute bottom-0 right-1/4 w-96 h-96 bg-accent/5 rounded-full blur-3xl pointer-events-none" />

      <div className="relative z-10 container mx-auto px-6 py-20">
        {/* Header */}
        <header className="text-center mb-16 fade-in-up">
          <div className="inline-flex items-center gap-3 mb-6">
            <div className="p-3 rounded-xl bg-primary/10 glow-border">
              <Container className="w-8 h-8 text-primary" />
            </div>
          </div>
          
          <h1 className="text-5xl md:text-6xl font-bold mb-4">
            <span className="text-foreground">Data </span>
            <span className="gradient-text glow-text">QueryAI</span>
          </h1>
          
          <p className="text-muted-foreground text-lg md:text-xl max-w-2xl mx-auto">
            Ask questions in plain English. Get insights from your MongoDB data instantly.
          </p>
        </header>

        {/* Search Bar */}
        <div className="mb-8" style={{ animationDelay: "0.2s" }}>
          <SearchBar onSearch={handleSearch} isLoading={isLoading} />
        </div>

        {/* Results */}
        <ResultDisplay
          query={query}
          naturalLanguageResult={naturalLanguageResult}
          isLoading={isLoading}
        />

        {/* Footer hint */}
        {!query && !isLoading && (
          <div className="text-center mt-20 fade-in-up" style={{ animationDelay: "0.4s" }}>
            <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-muted/50 text-muted-foreground text-sm">
              <span className="pulse-dot pl-4">Connected to MongoDB</span>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default Index;
