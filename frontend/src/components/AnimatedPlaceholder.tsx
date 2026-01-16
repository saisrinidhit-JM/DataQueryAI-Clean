import { useState, useEffect } from "react";

const PROMPTS = [
  "Show me all users who signed up last month",
  "What's the total revenue by product category?",
  "Find orders with status pending over 7 days",
  "List top 10 customers by purchase amount",
  "Get inventory items below restock threshold",
  "Show active subscriptions expiring this week",
  "Count users grouped by country",
  "Find transactions above $1000 today",
];

interface AnimatedPlaceholderProps {
  isTyping: boolean;
}

const AnimatedPlaceholder = ({ isTyping }: AnimatedPlaceholderProps) => {
  const [currentIndex, setCurrentIndex] = useState(0);
  const [isAnimating, setIsAnimating] = useState(false);

  useEffect(() => {
    if (isTyping) return;

    const interval = setInterval(() => {
      setIsAnimating(true);
      setTimeout(() => {
        setCurrentIndex((prev) => (prev + 1) % PROMPTS.length);
        setIsAnimating(false);
      }, 300);
    }, 3500);

    return () => clearInterval(interval);
  }, [isTyping]);

  if (isTyping) return null;

  return (
    <span
      className={`text-muted-foreground/60 pointer-events-none transition-all duration-300 ${
        isAnimating ? "opacity-0 translate-y-[-10px]" : "opacity-100 translate-y-0"
      }`}
    >
      {PROMPTS[currentIndex]}
    </span>
  );
};

export default AnimatedPlaceholder;
