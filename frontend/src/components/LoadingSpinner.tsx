import { Loader2 } from "lucide-react";

export function LoadingSpinner() {
  return (
    <div className="flex flex-col items-center justify-center py-12 space-y-4 animate-fade-in">
      <div className="relative">
        <div className="w-16 h-16 rounded-full border-4 border-primary/20"></div>
        <Loader2 className="w-16 h-16 text-primary absolute top-0 left-0 animate-spin" />
      </div>
      <div className="text-center space-y-2">
        <p className="text-foreground font-medium">Extraindo dados...</p>
        <p className="text-muted-foreground text-sm">Isso pode levar até 10 segundos</p>
      </div>
    </div>
  );
}
