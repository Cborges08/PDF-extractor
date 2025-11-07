import { CheckCircle2, Copy, Clock } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Progress } from "@/components/ui/progress";
import { toast } from "sonner";

interface ResultCardProps {
  data: any;
  confidence?: number;
  executionTime?: number;
}

export function ResultCard({ data, confidence = 95, executionTime = 8.5 }: ResultCardProps) {
  const handleCopy = () => {
    navigator.clipboard.writeText(JSON.stringify(data, null, 2));
    toast.success("JSON copiado para a área de transferência!");
  };

  return (
    <div className="space-y-4 animate-fade-in">
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-2">
          <CheckCircle2 className="w-5 h-5 text-success" />
          <h3 className="font-semibold text-foreground">Dados Extraídos</h3>
        </div>
        <Button
          variant="outline"
          size="sm"
          onClick={handleCopy}
          className="rounded-lg"
        >
          <Copy className="w-4 h-4 mr-2" />
          Copiar JSON
        </Button>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div className="p-4 rounded-xl bg-card border border-border">
          <p className="text-sm text-muted-foreground mb-2">Confiança</p>
          <Progress value={confidence} className="h-2 mb-2" />
          <p className="text-2xl font-bold text-foreground">{confidence}%</p>
        </div>
        <div className="p-4 rounded-xl bg-card border border-border">
          <p className="text-sm text-muted-foreground mb-2">Tempo de Execução</p>
          <div className="flex items-center gap-2">
            <Clock className="w-5 h-5 text-primary" />
            <p className="text-2xl font-bold text-foreground">{executionTime}s</p>
          </div>
        </div>
      </div>

      <div className="relative rounded-2xl bg-card border border-border shadow-card overflow-hidden">
        <div className="absolute top-0 left-0 right-0 h-1 bg-gradient-primary"></div>
        <pre className="p-6 overflow-x-auto text-sm font-mono">
          <code className="text-foreground">{JSON.stringify(data, null, 2)}</code>
        </pre>
      </div>
    </div>
  );
}
