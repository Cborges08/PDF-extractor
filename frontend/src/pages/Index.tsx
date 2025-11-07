import { useState } from "react";
import { Header } from "@/components/Header";
import { Footer } from "@/components/Footer";
import { FileUpload } from "@/components/FileUpload";
import { JsonEditor } from "@/components/JsonEditor";
import { ResultCard } from "@/components/ResultCard";
import { LoadingSpinner } from "@/components/LoadingSpinner";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { toast } from "sonner";
import { Sparkles } from "lucide-react";
import axios from "axios";
const apiUrl = import.meta.env.VITE_API_URL;

const Index = () => {
  const [label, setLabel] = useState("");
  const [schema, setSchema] = useState(`{\n  "cpf": "número de identificação de pessoa física em formato XXX.XXX.XXX-XX",\n  "nome": "nome completo"\n}`);
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  const [result, setResult] = useState<any>(null);
  const handleExtract = async () => {
    if (!label.trim()) {
      toast.error("Por favor, insira o label do documento");
      return;
    }
    if (!schema.trim()) {
      toast.error("Por favor, insira o schema de extração");
      return;
    }
    if (!selectedFile) {
      toast.error("Por favor, selecione um arquivo PDF");
      return;
    }

    try {
      JSON.parse(schema);
    } catch {
      toast.error("Schema JSON inválido");
      return;
    }

    setIsLoading(true);
    setResult(null);

    const formData = new FormData();
    formData.append("label", label);
    formData.append("extraction_schema", schema);
    formData.append("pdf", selectedFile);

    try {
      const response = await axios.post(`${apiUrl}/extract`, formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });

      setResult(response.data);
      toast.success("Dados extraídos com sucesso!");
    } catch (error) {
      console.error(error);
      toast.error("Erro ao extrair dados do documento");
    } finally {
      setIsLoading(false);
    }
  };

  return <div className="flex min-h-screen flex-col bg-background">
      <Header />
      
      <main className="flex-1 pt-24 pb-12">
        <div className="container mx-auto px-4 max-w-4xl">
          <div className="text-center mb-12">
            <h2 className="text-5xl md:text-7xl font-bold mb-4 leading-tight">
              <span className="text-gradient-primary">Extração Inteligente</span>
              <br />
              <span className="text-foreground">de Dados com IA</span>
            </h2>
            <p className="text-muted-foreground text-lg max-w-2xl mx-auto">
              Envie seu documento e extraia dados estruturados com precisão de IA
            </p>
          </div>

          <div className="rounded-3xl bg-card border border-border shadow-lg p-6 md:p-8 space-y-6">
            <div className="space-y-2">
              <Label htmlFor="label" className="text-foreground font-medium">
                Tipo de Documento (Label)
              </Label>
              <Input id="label" placeholder="Ex: fatura, contrato, nota fiscal..." value={label} onChange={e => setLabel(e.target.value)} className="rounded-xl border-border bg-background text-foreground" />
            </div>

            <div className="space-y-2">
              <Label htmlFor="schema" className="text-foreground font-medium">
                Schema de Extração (JSON)
              </Label>
              <JsonEditor value={schema} onChange={setSchema} placeholder='{\n  "campo": "descrição do campo"\n}' />
            </div>

            <div className="space-y-2">
              <Label className="text-foreground font-medium">
                Arquivo PDF
              </Label>
              <FileUpload selectedFile={selectedFile} onFileSelect={setSelectedFile} />
            </div>

            <Button onClick={handleExtract} disabled={isLoading} className="w-full h-12 rounded-xl text-base font-bold gradient-primary hover:opacity-90 shadow-lg hover:shadow-xl transition-all">
              {isLoading ? "EXTRAINDO..." : <>
                  <Sparkles className="w-5 h-5 mr-2" />
                  SOLICITAR EXTRAÇÃO
                </>}
            </Button>
          </div>

          {isLoading && <div className="mt-8">
              <LoadingSpinner />
            </div>}

          {result && !isLoading && <div className="mt-8">
              <ResultCard data={result} confidence={95} executionTime={8.5} />
            </div>}
        </div>
      </main>

      
    </div>;
};
export default Index;