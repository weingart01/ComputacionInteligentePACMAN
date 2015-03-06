/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */

import java.io.*;
import java.io.FileNotFoundException;
import java.util.*;
import java.util.logging.Level;
import java.util.logging.Logger;
/**
 * @author weingart
 */
public class Etiquetador {

    /**
     * @param args the command line arguments
     */
    public static void main(String[] args) throws FileNotFoundException, UnsupportedEncodingException {
        // TODO code application logic here
        /* Si el argumento que enviamos al programa no es el adecuado, no podemos
         * realizar el etiquetado, por lo cual damos un mensaje de error. */
        if (args.length != 3){
            System.out.println("Error argumentos incorrectos");
            System.exit(0);
	}
        /* Obetenemos la direccion donde se encuentra el archivo */
        String direccion = args[0];
        /* Obtenemos el nombre del archivo a etiquetar */
        String archivo = args[1];
        /* Obtenemos */
        String texto_correcto = args[2];
        /* Pasams a leer el corpus */
        leerCorpus(direccion);
        HashMap< String, HashMap< String, Integer>> corpus2 = parserCorpus("./lexic.txt");
        etiquetarTexto(archivo);
        comparacionResultados(archivo + "_Etiquetado", texto_correcto);
    }

    static void leerCorpus(String path) {
        String line = "";
        String palabra;
        String categoria;
        int nveces;
        /* Utilizamos el Hashmap debido a su rapido acceso y lo mapeamos de la 
         * siguiente manera [palabra, categoria, nveces]*/
        HashMap< String, HashMap< String, Integer>> corpus = new HashMap<String, HashMap<String, Integer>>();
        try {
            BufferedReader stop = new BufferedReader(new InputStreamReader(new FileInputStream(path), "ISO-8859-1"));
            /* mientras tengamos lineas por leer */
            while ((line = stop.readLine()) != null) {
                /* Creamos los tokens mediante el split de la linea que estamos
                 * leyendo actualmente. */
                String[] tokens = line.split("\t");
                /* Pasamos a poner las primeras letras que posiblemente puedan
                 * ser mayusculas, en minusculas, de esta manera no diferenciaremos
                 * las palabras que empiecen una oracion de otra que este en medio
                 * de la palabra. ej: Un == un 
                 * Un problema seria palabras como papa y Papa que obviamente tienen
                 * significados diferentes. */
                palabra = tokens[0].toLowerCase();
                /* Cogemos la categoria a la que corresponde la palabra. */
                categoria = tokens[1];
                if (corpus.containsKey(palabra)) {
                    HashMap<String, Integer> viejo = corpus.get(palabra);
                    if (viejo.containsKey(categoria)) {
                        nveces = viejo.get(categoria);
                        ++nveces;
                        viejo.put(categoria, nveces);
                    } else {
                        viejo.put(categoria, 1);
                    }
                } else {
                    HashMap<String, Integer> nuevo = new HashMap<String, Integer>();
                    nuevo.put(tokens[1], 1);
                    corpus.put(tokens[0], nuevo);
                }
            }
			try {
            	escribircorpus(corpus);
        	} catch (UnsupportedEncodingException ex) {
            	Logger.getLogger(Etiquetador.class.getName()).log(Level.SEVERE, null, ex);
        	} catch (FileNotFoundException ex) {
            	Logger.getLogger(Etiquetador.class.getName()).log(Level.SEVERE, null, ex);
        	} catch (IOException ex) {
            	Logger.getLogger(Etiquetador.class.getName()).log(Level.SEVERE, null, ex);
        	}

        } catch (IOException e) {
        }

        
    }

    static void etiquetarTexto(String path) throws FileNotFoundException, UnsupportedEncodingException {
        HashMap< String, HashMap<String, Integer>> corpus = parserCorpus("./lexic.txt");
        File fichero = new File(path + "_Etiquetado");
        if (fichero.exists()) {
            fichero.delete();
        }
        double contador = 0;
        double mas = 0;
        try {
            BufferedWriter Fescribe = new BufferedWriter(new OutputStreamWriter(new FileOutputStream(path + "_Etiquetado", true), "ISO-8859-1"));
            BufferedReader stop = new BufferedReader(new InputStreamReader(new FileInputStream(path), "ISO-8859-1"));
            String line;
            String palabra;
            String palabra2;
            String maximo = "";
            int maxveces = 0;
            int veces;
            String anterior = "";
            while ((line = stop.readLine()) != null) {
                String[] tokens = line.split("\t");
                palabra2 = tokens[0];
                palabra = tokens[0].toLowerCase();

                if (corpus.containsKey(palabra)) {
                    ++contador;
                    HashMap<String, Integer> añadido = corpus.get(palabra);
                    if (añadido.size() > 1) {
                        ++mas;
                    }
                    Iterator it = añadido.entrySet().iterator();
                    maxveces = 0;
                    while (it.hasNext()) {
                        Map.Entry e = (Map.Entry) it.next();
                        veces = (Integer) e.getValue();
                        if (maxveces < veces) {
                            maxveces = veces;
                            maximo = (String) e.getKey();
                        }
                    }
                    anterior = maximo;
                    Fescribe.write(palabra2 + "\t" + maximo + "\r\n");
                } else {
                    if (palabra2.charAt(0) <= 'Z' && palabra2.charAt(0) >= 'A') {
                        Fescribe.write(palabra2 + "\t" + "NP" + "\r\n");
                    } else if (palabra2.charAt(0) <= '9' && palabra2.charAt(0) >= '0') {
                        Fescribe.write(palabra2 + "\t" + "Num" + "\r\n");
                    } else if (anterior.equals("Det")) {
                        Fescribe.write(palabra2 + "\t" + "NC" + "\r\n");
                    } else if (anterior.equals("V")) {
                        Fescribe.write(palabra2 + "\t" + "Prep" + "\r\n");
                    } else if (anterior.equals("Pron")) {
                        Fescribe.write(palabra2 + "\t" + "V" + "\r\n");
                    } else {
                        String corregida = corregir(palabra, corpus);
                        if (corregida == null) {
                            Fescribe.write(palabra2 + "\t" + "V" + "\r\n");
                        } else {
                            ++contador;
                            HashMap<String, Integer> añadido = corpus.get(corregida);
                            if (añadido.size() > 1) {
                                ++mas;
                            }
                            Iterator it = añadido.entrySet().iterator();
                            maxveces = 0;
                            while (it.hasNext()) {
                                Map.Entry e = (Map.Entry) it.next();
                                veces = (Integer) e.getValue();
                                if (maxveces < veces) {
                                    maxveces = veces;
                                    maximo = (String) e.getKey();
                                }
                            }
                            anterior = maximo;
                            Fescribe.write(palabra2 + "\t" + maximo + "\r\n");

                        }
                    }
                }
            }
            System.out.println("Numero de duplicados : " + mas + ". Palabras encontradas en corpus : " + contador);
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
                String[] tokens1 = line1.split("\t");
                String[] tokens2 = line2.split("\t");
                if (tokens1[0].equalsIgnoreCase(tokens2[0]) && tokens1[1].equals(tokens2[1])) {
                    ++acertadas;
                } else {

                    if (!tokens1[0].equalsIgnoreCase(tokens2[0]) && tokens1[1].equals(tokens2[1])) {
                        System.out.println("Error \n");
                        System.out.println("Palabra1: " + tokens1[0] + ", Cat : " + tokens1[1] + ". Palabra2: " + tokens2[0] + ", Cat : " + tokens2[1] + "\n");
                    }
                    if (tokens1[1].equals("NOAPARECE")) {
                        ++noaparece;
                    } else {
                        ++fallo;
                    }
                }
                ++totales;
            }

        } catch (IOException e) {
        }
        System.out.println("Acertadas : " + acertadas + ". Totales : " + totales + ". Falladas : " + fallo);
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
        try (BufferedWriter Fescribe = new BufferedWriter(new OutputStreamWriter(new FileOutputStream("./lexic.txt", true), "utf-8"))) {
            for (Map.Entry e2 : corpus.entrySet()) {
                HashMap<String, Integer> viejo = (HashMap<String, Integer>) e2.getValue();
                for (Map.Entry e : viejo.entrySet()) {
                    Fescribe.write((String) e2.getKey() + "\t" + (String) e.getKey() + "\t" + (Integer) e.getValue() + "\r\n");
                }
            }
        }
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
