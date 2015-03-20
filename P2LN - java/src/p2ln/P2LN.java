/*
 * To change this template, choose Tools | Templates
 * and open the template in the editor.
 */
package p2ln;

import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.File;
import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.FileOutputStream;
import java.io.FileReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.OutputStreamWriter;
import java.io.UnsupportedEncodingException;
import java.util.HashMap;
import java.util.HashSet;
import java.util.Iterator;
import java.util.Map;

/**
 *
 * @author U74473
 */
public class P2LN {

    /**
     * @param args the command line arguments
     */
    public static void main(String[] args) throws FileNotFoundException, UnsupportedEncodingException, IOException {
        // TODO code application logic here
		/*if (args.length != 3){
         System.out.println("Error argumentos incorrectos");
         System.exit(0);
         }*/
        String palabraaestudio = args[0];
        int significados = 1;
        boolean fin = true;
        while (fin) {
            File fichero = new File(palabraaestudio + significados + ".txt");
            if (fichero.exists()) {
                ++significados;
            } else {
                --significados;
                fin = false;
            }
        }
        int i = 0;
        int[] numero = new int[significados];
        HashMap< String, HashMap< Integer, Integer>> corpus = new HashMap<String, HashMap<Integer, Integer>>();
        String test = palabraaestudio + ".test.txt";
        String correcto = palabraaestudio + ".key.txt";
        String resultado  = test + "_Etiquetado.txt";
        String baseline = test + "_Etiquetado2.txt";
        while (i < significados) {
            String path = palabraaestudio + (i + 1) + ".txt";
            numero[i] = leerCorpus(path, corpus, (i + 1), significados);
            System.out.println("Frases " + (i + 1) + " : " + numero[i]);
            ++i;
        }
        etiquetarTexto(test, corpus, numero);
        etiquetarBaseline(test, numero);
        comparacionResultados(resultado, correcto);
        comparacionResultados(baseline, correcto);
    }

    static int leerCorpus(String path, HashMap< String, HashMap< Integer, Integer>> corpus, int mean, int significados) {
        String line;
        String palabra;
        String categoria;
        int veces;
        HashSet<String> stoptags = new HashSet<String>();
        stoptags.add("A0");
        stoptags.add("AQ");
        stoptags.add("CC");
        stoptags.add("CS");
        stoptags.add("NC");
        stoptags.add("NP");
        stoptags.add("P0");
        stoptags.add("PD");
        stoptags.add("PI");
        stoptags.add("PN");
        stoptags.add("PP");
        stoptags.add("PR");
        stoptags.add("PT");
        stoptags.add("PX");
        stoptags.add("RG");
        stoptags.add("RN");
        stoptags.add("UH");
        stoptags.add("VM");
        stoptags.add("VS");
        int numfrases = 0;
        boolean print = false;
        try {
            BufferedReader stop = new BufferedReader(new InputStreamReader(new FileInputStream(path), "ISO-8859-1"));
            HashMap<String, String> sentence = new HashMap<String, String>();

            while ((line = stop.readLine()) != null) {
                sentence.clear();
                ++numfrases;
                String[] tokens = line.split(" ");
                int i = 0;
                while (i < tokens.length) {
                    if (i > 60 && i < 120) {
                        if (!sentence.containsKey(tokens[i])) {
                            sentence.put(tokens[i], tokens[i + 60]);
                        }
                    }
                    ++i;
                }
                for (Map.Entry e : sentence.entrySet()) {
                    String word = (String) e.getKey();
                    String tag = (String) e.getValue();
                    if (stoptags.contains(tag)) {
                        if (corpus.containsKey(word)) {
                            HashMap<Integer, Integer> little = corpus.get(word);
                            veces = little.get(mean);
                            ++veces;
                            little.put(mean, veces);
                            corpus.put(word, little);

                        } else {
                            HashMap<Integer, Integer> little = new HashMap<Integer, Integer>();
                            int j = 1;
                            while (j <= significados) {
                                little.put(j, 0);
                                ++j;
                            }
                            little.put(mean, 1);
                            corpus.put(word, little);
                        }
                    }
                }

            }

        } catch (IOException e) {
        }

        return numfrases;
    }

    static void etiquetarBaseline(String path, int[] nummean) {
        File fichero = new File(path + "_Etiquetado2.txt");
        if (fichero.exists()) {
            fichero.delete();
        }
        int i = 0;
        int max = 0;
        int frases = 0;
        while (i < nummean.length) {
            if (nummean[i] > frases) {
                frases = nummean[i];
                max = i;
            }
            ++i;
        }
        ++max;
        try {
            int frase = 0;
            String line;
            BufferedWriter Fescribe = new BufferedWriter(new OutputStreamWriter(new FileOutputStream(path + "_Etiquetado2.txt", true), "ISO-8859-1"));
            BufferedReader stop = new BufferedReader(new InputStreamReader(new FileInputStream(path), "ISO-8859-1"));
            while ((line = stop.readLine()) != null) {
                ++frase;
                Fescribe.write(frase + " " + max);
                Fescribe.write("\r\n");
            }
            Fescribe.close();
        } catch (IOException e) {
        }
    }

    static void etiquetarTexto(String path, HashMap< String, HashMap< Integer, Integer>> corpus, int[] nummean) throws FileNotFoundException, UnsupportedEncodingException {

        //HashMap< String, HashMap<String, Integer>> corpus = parserCorpus("./lexic.txt");
        File fichero = new File(path + "_Etiquetado.txt");
        if (fichero.exists()) {
            fichero.delete();
        }

        String words[] = new String[60];
        String tags[] = new String[60];
        double contador = 0;
        double mas = 0;
        String line;
        int numfrases = 0;
        int frase = 0;
        try {
            BufferedWriter Fescribe = new BufferedWriter(new OutputStreamWriter(new FileOutputStream(path + "_Etiquetado.txt", true), "ISO-8859-1"));
            BufferedReader stop = new BufferedReader(new InputStreamReader(new FileInputStream(path), "ISO-8859-1"));
            while ((line = stop.readLine()) != null) {
                ++frase;
                ++numfrases;
                String[] tokens = line.split(" ");
                int k = 0;
                while (k < tokens.length) {
                    ++k;
                }
                int i = 0;
                int j = 0;
                while (i < tokens.length) {
                    if (i >= k / 3 && i < 2 * k / 3) {
                        words[j] = tokens[i];
                        tags[j] = tokens[i + (k / 3)];
                        ++j;
                    }
                    ++i;
                }
                i = 0;
                double values[] = new double[nummean.length];
                double frasestotales = 0;
                double aux;
                while (i < nummean.length) {
                    aux = nummean[i];
                    frasestotales += nummean[i];
                    ++i;
                }

                j = 0;
                while (j < nummean.length) {
                    double aux2;
                    i = 0;
                    values[j] = nummean[j] / frasestotales;
                    while (i < k / 3) {
                        if (corpus.containsKey(words[i])) {
                            HashMap< Integer, Integer> numveces = corpus.get(words[i]);
                            aux2 = numveces.get(j + 1);
                            if (aux2 == 0) {
                                values[j] = values[j] * (1 / frasestotales);
                            } else {
                                values[j] = values[j] * (aux2 / nummean[j]);
                            }
                        } else {
                            values[j] = values[j] * (1 / frasestotales);
                        }
                        ++i;
                    }
                    ++j;
                }
                i = 0;
                double max = values[i];
                int sigmax = 0;
                while (i < values.length) {
                    if (values[i] > max) {
                        max = values[i];
                        sigmax = i;
                    }
                    ++i;
                }
                Fescribe.write(frase + " " + (sigmax + 1));
                Fescribe.write("\r\n");
            }
            Fescribe.close();
        } catch (IOException e) {
        }

    }

    static double comparacionResultados(String path1, String path2) {
        double acertadas = 0;
        double totales = 0;
        double noaparece = 0;
        double fallo = 0;
        try {
            BufferedReader original = new BufferedReader(new InputStreamReader(new FileInputStream(path1), "ISO-8859-1"));
            BufferedReader correcto = new BufferedReader(new InputStreamReader(new FileInputStream(path2), "ISO-8859-1"));
            String line1;
            String line2;
            while ((line1 = original.readLine()) != null && (line2 = correcto.readLine()) != null) {
                String[] tokens1 = line1.split(" ");
                String[] tokens2 = line2.split(" ");
                if (Integer.parseInt(tokens1[1]) == Integer.parseInt(tokens2[1])) {
                    ++acertadas;
                }
                ++totales;
            }

        } catch (IOException e) {
        }
        System.out.println("Porcentaje de acierto : " + (acertadas / totales));
        if (totales != 0) {
            return (acertadas / totales);
        }
        return 0;
    }

    static void escribircorpus(HashMap< String, HashMap< String, Integer>> corpus) throws UnsupportedEncodingException, FileNotFoundException, IOException {
        File fichero = new File("./lexic.txt");
        if (fichero.exists()) {
            fichero.delete();
        }
        BufferedWriter Fescribe = new BufferedWriter(new OutputStreamWriter(new FileOutputStream("./lexic.txt", true), "utf-8"));
        Iterator it2 = corpus.entrySet().iterator();
        while (it2.hasNext()) {
            Map.Entry e2 = (Map.Entry) it2.next();
            HashMap<String, Integer> viejo = (HashMap<String, Integer>) e2.getValue();
            Iterator it = viejo.entrySet().iterator();
            while (it.hasNext()) {
                Map.Entry e = (Map.Entry) it.next();
                Fescribe.write((String) e2.getKey() + "\t" + (String) e.getKey() + "\t" + (Integer) e.getValue() + "\r\n");
            }
        }
        Fescribe.close();
    }

    static HashMap< String, HashMap< String, Integer>> parserCorpus(String path) throws FileNotFoundException {
        HashMap< String, HashMap< String, Integer>> corpus = new HashMap<String, HashMap<String, Integer>>();
        String line;
        String palabra;
        String categoria;
        int veces;
        try {
            BufferedReader stop = new BufferedReader(new FileReader(path));
            while ((line = stop.readLine()) != null) {
                String[] tokens = line.split("\t");
                palabra = tokens[0];
                categoria = tokens[1];
                veces = Integer.parseInt(tokens[2]);
                if (corpus.containsKey(palabra)) {
                    HashMap<String, Integer> viejo = corpus.get(palabra);
                    viejo.put(categoria, veces);
                } else {
                    HashMap<String, Integer> nuevo = new HashMap<String, Integer>();
                    nuevo.put(categoria, veces);
                    corpus.put(palabra, nuevo);
                }
            }

        } catch (IOException e) {
        }
        return corpus;
    }

    static String corregir(String word, HashMap< String, HashMap< String, Integer>> corpus) {

        Iterator it2 = corpus.entrySet().iterator();
        String palabra;

        while (it2.hasNext()) {
            Map.Entry e2 = (Map.Entry) it2.next();
            palabra = (String) e2.getKey();
            boolean encontrado = true;
            if (word.length() == palabra.length()) {
                int i = 0;
                boolean diferente = false;
                while (i < word.length() && encontrado) {
                    if (palabra.charAt(i) != word.charAt(i)) {
                        if (diferente) {
                            encontrado = false;
                        } else {
                            diferente = true;
                        }
                    }
                    ++i;
                }
                if (encontrado) {
                    return palabra;
                }
            }
        }
        return null;
    }
}
