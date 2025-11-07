import { Button } from "@/components/ui/button";
export function Header() {
  return <header className="fixed top-0 left-0 right-0 h-16 bg-background border-b border-border z-50">
      <div className="h-full flex items-center justify-between">
        <div className="px-8 flex items-center gap-3">
          <div className="flex items-center gap-2">
            <span className="text-2xl font-bold tracking-tight text-foreground">ENTER</span>
            <div className="w-3 h-3 bg-primary"></div>
          </div>
        </div>
        
      </div>
    </header>;
}