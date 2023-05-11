Evolventenzahnräder
===================

Die Grundlagen von Evolventenzahnrädern sind sehr gut beschrieben: https://www.tec-science.com/de/getriebe-technik/evolventenverzahnung/eingriff-linie-strecke-winkel-waelzkreis-verzahnungsgesetz/
Die Konstruktion findet man hier: https://www.tec-science.com/de/getriebe-technik/evolventenverzahnung/evolventen-zahnrad-geometrie/

Die Berechnung der Evolvente: https://www.tec-science.com/de/getriebe-technik/evolventenverzahnung/berechnung-von-zahnrader/

Evolventenzahnräder sind beschrieben durch ihre Zahngröße oder auch Modul _m_, die Zahnform bzw. der Eingriffswinkel alpha und die Anzahl der Zähne _z_.
Der Normaleingriffswinkel alpha_0 beträgt 20°. Dieser kann auch variieren.
Zahnräder mit unterschiedlicher Zähnezahl aber gleichem Modul greifen ineinander.


Geometrie der Zahnräder
-----------------------

In DIN 780 sind die Festlegungen dazu getroffen.
Die wichtigste Kenngröße eines Zahnrads sein Teilkreisdurchmesser/-radius.
Auf dem Teilkreis ist die Dicke des Zahnes und die Lücke gleich groß.
Der Teilkreisdurchmesser _d_ ist festgelegt als:

    _d0_ = _m_ * _z_

oder

    _r0_ = _m_ * _z_ / 2.

Die Zahlteilung _p0_ am Teilkreis ist damit

    _p0_ = _m_ * &pi;

Die Höhe des Kopfes _hk_ eines Zahnes entspricht dem Modul _m_.
Daraus ergibt sich ein Kopfkreisradius von 

    _rk_ = _rd_ + m

und ein Fußkreisradius von 

    _rf_ = _rd_ - m

Der Winkel der Zähne (Mitte) zueinander ergibt sich aus der Zähnezahl:

    &alpha; = 2 * &pi; / z

Der Winkel von der Mitte eines Zahnes zum Schnittpunkt des Zahnes auf dem Teilkreis ist:

    &beta; = &alpha / 4

Die Bogenlänge auf dem Fußkreis _ld_,um über die Evolvente den Schnittpunkt des Zahnes auf dem Teilkreis zu erhalten, ist:

    _ld_ = SQR(_rd_^2 - _rf_^2)

Die Länge des Bogens für den Kopfpunkt eines Zahnes ist entsprechend:

    _lk_ = SQR(_rk_^2 - _rf_^2)

Daraus ergeben sich jeweils die beiden Winkel:

    &gamma; = _ld_ / (_rf_ * 2 * &pi;)
    &delta; = _lk_ / (_rf_ * 2 * &pi;)

Approximation mit Bezierkurven
------------------------------

In einer 2D-Darstellung können die Zähne sehr gut mit Bezierkurven approximiert werden.
Es bietet sich an, für jede Flanke eines Zahnes jeweils zwei Bezierkurfen zu verwenden:
 * Die erste Bezierkurve vom Fußpunkt bis zum Teilkreis.
 * Die zweite Bezierkurve vom Teilkreis bis zum Kopfpunkt.

Für die absteigende Flanke einsprechend vom Kopfpunkt bis zum Teilkreis und vom Teilkreis bis zum Fußpunkt.

Um dies zu erreichen, müssen für jeden Zahn des Zahnrads 6 Stützpunkte mit ihren Normalen/Tangenten berechent werden.

Jeder Stützpunkt kann durch einen Winkeloffset und den entspechenden Radius beschrieben werden.
Die folgenden Tabelle gibt jeweils den Radius und den Winkeloffset an.

    _p1_ = (_rf_, &alpha; / 4 - &gamma;)
    _p2_ = (_rd_, &alpha; / 4)
    _p3_ = (_rk_, &alpha; / 4 - &gamma; + &delta;)
    _p4_ = (_rk_, &aplha; * 3 / 4 - (&gamma; + &delta;))
    _p5_ = (_rd_, &alpha; * 3 / 4)
    _p6_ = (_rf_, &alpha; * 3 / 4 + &gamma;)

Die Tangenten entsprechen den jeweiligen Winkel.
Aus diesen kann dann zusammen mit den jeweiligen Punkten der dritte Stützpunkt für die Bezierkurve berechnet werden.
