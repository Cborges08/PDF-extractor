import { Textarea } from "@/components/ui/textarea";

interface JsonEditorProps {
  value: string;
  onChange: (value: string) => void;
  placeholder?: string;
}

export function JsonEditor({ value, onChange, placeholder }: JsonEditorProps) {
  return (
    <Textarea
      value={value}
      onChange={(e) => onChange(e.target.value)}
      placeholder={placeholder}
      className="min-h-[200px] font-mono text-sm rounded-2xl border-border bg-background text-foreground shadow-card resize-none focus:ring-2 focus:ring-primary focus:border-transparent transition-all"
    />
  );
}
