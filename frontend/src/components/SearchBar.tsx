import { useState, useRef } from "react";
import { Search, ArrowRight, Loader2 } from "lucide-react";
import AnimatedPlaceholder from "./AnimatedPlaceholder";

interface SearchBarProps {
  onSearch: (query: string) => void;
  isLoading?: boolean;
}

const SearchBar = ({ onSearch, isLoading = false }: SearchBarProps) => {
  const [query, setQuery] = useState("");
  const [isFocused, setIsFocused] = useState(false);
  const inputRef = useRef<HTMLInputElement>(null);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (query.trim() && !isLoading) {
      onSearch(query.trim());
    }
  };

  const isTyping = query.length > 0;

  return (
    <form onSubmit={handleSubmit} className="w-full max-w-3xl mx-auto">
      <div
        className={`relative glass-panel transition-all duration-300 ${isFocused ? "search-glow scale-[1.02]" : ""
          }`}
      >
        <div className="flex items-center px-5 py-4">
          <Search className="w-5 h-5 text-muted-foreground mr-4 flex-shrink-0" />

          <div className="relative flex-1">
            <input
              ref={inputRef}
              type="text"
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              onFocus={() => setIsFocused(true)}
              onBlur={() => setIsFocused(false)}
              className="w-full bg-transparent text-foreground text-lg outline-none placeholder:text-transparent"
              placeholder="Enter your query..."
              disabled={isLoading}
            />
            {!isTyping && !isFocused && (
              <div className="absolute inset-0 flex items-center pointer-events-none">
                <AnimatedPlaceholder isTyping={isTyping} />
              </div>
            )}
          </div>

          <button
            type="submit"
            disabled={!query.trim() || isLoading}
            className="ml-4 p-2.5 rounded-xl bg-primary text-primary-foreground disabled:opacity-30 disabled:cursor-not-allowed hover:bg-primary/90 transition-all duration-200 hover:scale-105 active:scale-95"
          >
            {isLoading ? (
              <Loader2 className="w-5 h-5 animate-spin" />
            ) : (
              <ArrowRight className="w-5 h-5" />
            )}
          </button>
        </div>

        {/* Subtle gradient line at bottom */}
        <div className="absolute bottom-0 left-1/2 -translate-x-1/2 w-1/2 h-px bg-gradient-to-r from-transparent via-primary/50 to-transparent" />
      </div>

      <p className="text-center text-muted-foreground/60 text-sm mt-4">
        Ask in natural language • Results powered by AI
      </p>
    </form>
  );
};

export default SearchBar;
