import { MessageSquare, Sparkles } from "lucide-react";

interface ResultDisplayProps {
  query: string;
  naturalLanguageResult: string | null;
  isLoading: boolean;
}

const ResultDisplay = ({
  query,
  naturalLanguageResult,
  isLoading,
}: ResultDisplayProps) => {
  if (!query && !isLoading) return null;

  return (
    <div className="w-full max-w-4xl mx-auto mt-12 fade-in-up">
      {/* Natural Language Response */}
      <div className="glass-panel p-8 relative overflow-hidden">
        {/* Decorative gradient */}
        <div className="absolute top-0 left-0 w-full h-1 bg-gradient-to-r from-transparent via-primary to-transparent opacity-50" />
        
        <div className="flex items-start gap-4">
          <div className="p-3 rounded-xl bg-primary/10 border border-primary/20 shrink-0">
            <Sparkles className="w-6 h-6 text-primary" />
          </div>
          
          <div className="flex-1 min-w-0">
            <div className="flex items-center gap-2 mb-3">
              <MessageSquare className="w-4 h-4 text-muted-foreground" />
              <span className="text-sm text-muted-foreground font-medium">AI Response</span>
            </div>
            
            {isLoading ? (
              <div className="space-y-3">
                <div className="h-5 bg-muted/50 rounded-lg animate-pulse w-full" />
                <div className="h-5 bg-muted/50 rounded-lg animate-pulse w-4/5" />
                <div className="h-5 bg-muted/50 rounded-lg animate-pulse w-3/5" />
                <div className="h-5 bg-muted/50 rounded-lg animate-pulse w-2/3" />
              </div>
            ) : (
              <p className="text-foreground text-lg leading-relaxed">
                {naturalLanguageResult || "Processing your query..."}
              </p>
            )}
          </div>
        </div>
        
        {/* Query reference */}
        {query && !isLoading && (
          <div className="mt-6 pt-4 border-t border-border/50">
            <p className="text-sm text-muted-foreground">
              <span className="text-muted-foreground/70">Query:</span>{" "}
              <span className="text-foreground/80 font-mono">{query}</span>
            </p>
          </div>
        )}
      </div>
    </div>
  );
};

export default ResultDisplay;
